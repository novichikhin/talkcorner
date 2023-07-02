import uuid
from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED
)

from talkcorner.common import types, exceptions
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.common.types import errors
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.dependencies.security import CryptContextMarker
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.api.api_v1.responses.user import user_auth_responses
from talkcorner.server.core.auth import authenticate_user, create_access_token, get_user
from talkcorner.server.core.security import get_password_hash

router = APIRouter()


@router.post(
    "/login",
    response_model=types.Token,
    responses={
        HTTP_401_UNAUTHORIZED: {
            "description": "Wrong username (email) or password error",
            "model": errors.WrongUsernameOrPassword
        }
    }
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        crypt_context: CryptContext = Depends(CryptContextMarker),
        settings: types.Setting = Depends(SettingsMarker)
):
    user: types.User = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        holder=holder,
        crypt_context=crypt_context
    )

    access_token = create_access_token(payload={"user_id": str(user.id)}, settings=settings)

    return types.Token(access_token=access_token, token_type="bearer")


@router.get(
    "/",
    response_model=list[types.User],
    dependencies=[Depends(get_user)],
    response_model_exclude={"email", "email_token", "email_verified", "password"},
    responses=user_auth_responses
)
async def read_all(
        offset: int = 0,
        limit: int = 5,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    users = await holder.user.read_all(offset=offset, limit=limit)

    return [types.User.from_dto(user=user) for user in users]


@router.get(
    "/{id}",
    response_model=types.User,
    dependencies=[Depends(get_user)],
    response_model_exclude={"email", "email_token", "email_verified", "password"},
    responses=user_auth_responses | {
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | errors.UserNotFound
        }
    }
)
async def read(id: uuid.UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    user = await holder.user.read_by_id(user_id=id)

    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return types.User.from_dto(user=user)


@router.post(
    "/",
    response_model=types.User,
    response_model_exclude={"password", "email_token"},
    responses={
        HTTP_409_CONFLICT: {"model": Union[errors.EmailAlreadyExists, errors.UsernameAlreadyExists]},
        HTTP_400_BAD_REQUEST: {"description": "Unable to create user error", "model": errors.UnableCreateUser}
    }
)
async def create(
        user_create: types.UserCreate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        crypt_context: CryptContext = Depends(CryptContextMarker)
):
    try:
        user = await holder.user.create(
            username=user_create.username,
            password=get_password_hash(crypt_context=crypt_context, password=user_create.password),
            email=user_create.email
        )
    except exceptions.EmailAlreadyExists:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User email already exists"
        )
    except exceptions.UsernameAlreadyExists:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User username already exists"
        )
    except exceptions.UnableInteraction:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to create user"
        )

    return types.User.from_dto(user=user)
