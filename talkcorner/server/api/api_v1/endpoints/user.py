import uuid
from typing import Union, List

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from nats.js import JetStreamContext
from passlib.context import CryptContext
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)

from talkcorner.common.settings.environments.app import AppSettings
from talkcorner.server.api.api_v1 import responses
from talkcorner.server.api.api_v1.core.auth import api_authenticate_user
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.dependencies.nats import NatsJetStreamMarker
from talkcorner.server.api.api_v1.dependencies.security import CryptContextMarker
from talkcorner.server.api.api_v1.dependencies.setting import SettingsMarker
from talkcorner.server.api.api_v1.responses.main import user_auth_responses
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.auth import Authorization
from talkcorner.server.schemas.user import User, UserCreate
from talkcorner.server.services.user import (
    login_user,
    get_users,
    get_user,
    verify_email_user,
    create_user
)

router = APIRouter()


@router.post(
    "/login",
    response_model=Authorization,
    responses={
        HTTP_401_UNAUTHORIZED: {
            "description": "Wrong username (email) or password error",
            "model": responses.WrongUsernameOrPassword
        }
    }
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    crypt_context: CryptContext = Depends(CryptContextMarker),
    settings: AppSettings = Depends(SettingsMarker)
):
    return await login_user(
        username=form_data.username,
        password=form_data.password,
        holder=holder,
        crypt_context=crypt_context,
        settings=settings
    )


@router.get(
    "/",
    response_model=List[User],
    dependencies=[Depends(api_authenticate_user())],
    response_model_exclude={"email", "email_token", "email_verified", "password"},
    responses=user_auth_responses
)
async def read_all(
    offset: int = Query(default=0, ge=0, le=500),
    limit: int = Query(default=5, ge=1, le=1000),
    holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    return await get_users(
        offset=offset,
        limit=limit,
        holder=holder
    )


@router.get(
    "/{id}",
    response_model=User,
    dependencies=[Depends(api_authenticate_user())],
    response_model_exclude={"email", "email_token", "email_verified", "password"},
    responses=user_auth_responses | {
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.UserNotFound
        }
    }
)
async def read(id: uuid.UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_user(user_id=id, holder=holder)


@router.get(
    "/email/verify/{id}",
    response_model=User,
    response_model_exclude={"password", "email_token"},
    responses=user_auth_responses | {
        HTTP_403_FORBIDDEN: {
            "model": Union[
                responses.EmailAlreadyConfirmed,
                responses.EmailTokenIncorrect
            ]
        }
    }
)
async def email_verify(
    id: uuid.UUID,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(
        api_authenticate_user(check_email_verified=False)
    )
):
    return await verify_email_user(
        email_token=id,
        holder=holder,
        user=user
    )


@router.post(
    "/",
    response_model=User,
    response_model_exclude={"password", "email_token"},
    responses={
        HTTP_409_CONFLICT: {
            "model": Union[
                responses.EmailAlreadyExists,
                responses.UsernameAlreadyExists
            ]
        }

    }
)
async def create(
    user_create: UserCreate,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    crypt_context: CryptContext = Depends(CryptContextMarker),
    js: JetStreamContext = Depends(NatsJetStreamMarker),
    settings: AppSettings = Depends(SettingsMarker)
):
    return await create_user(
        user_create=user_create,
        holder=holder,
        crypt_context=crypt_context,
        js=js,
        settings=settings
    )
