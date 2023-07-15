import json
import uuid
from typing import Union

import msgpack
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from nats.js import JetStreamContext
from passlib.context import CryptContext
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)

from talkcorner.common import types, exceptions
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.common.services.auth import create_access_token, create_refresh_token
from talkcorner.server.api.api_v1 import responses
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.dependencies.nats import NatsJetStreamMarker
from talkcorner.server.api.api_v1.dependencies.security import CryptContextMarker
from talkcorner.server.api.api_v1.dependencies.setting import SettingsMarker
from talkcorner.server.api.api_v1.responses.main import user_auth_responses
from talkcorner.server.core.auth import (
    authenticate_user,
    get_user,
    verify_refresh_token
)
from talkcorner.server.core.security import get_password_hash

router = APIRouter()


@router.post(
    "/login",
    response_model=types.Authentication,
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
        settings: types.Settings = Depends(SettingsMarker)
):
    user: types.User = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        holder=holder,
        crypt_context=crypt_context
    )

    payload = {
        "user_id": str(user.id)
    }

    access_token = create_access_token(
        payload=payload,
        secret_key=settings.authorize_access_token_secret_key,
        expire_minutes=settings.authorize_access_token_expire_minutes
    )

    refresh_token = create_refresh_token(
        payload=payload,
        secret_key=settings.authorize_refresh_token_secret_key,
        expire_minutes=settings.authorize_refresh_token_expire_minutes
    )

    return types.Authentication(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=types.AccessToken,
    responses={
        HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials error",
            "model": responses.NotValidateCredentials
        }
    }
)
async def refresh(
        refresh_token: types.RefreshToken = Depends(verify_refresh_token),
        settings: types.Settings = Depends(SettingsMarker)
):
    new_access_token = create_access_token(
        payload={"user_id": str(refresh_token.user_id)},
        secret_key=settings.authorize_access_token_secret_key,
        expire_minutes=settings.authorize_access_token_expire_minutes
    )

    return types.AccessToken(access_token=new_access_token, token_type="bearer")


@router.get(
    "/",
    response_model=list[types.User],
    dependencies=[Depends(get_user())],
    response_model_exclude={"email", "email_token", "email_verified", "password"},
    responses=user_auth_responses
)
async def read_all(
        offset: int = Query(default=0, ge=0, le=500),
        limit: int = Query(default=5, ge=1, le=1000),
        holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    users = await holder.user.read_all(offset=offset, limit=limit)

    return [types.User.from_dto(user=user) for user in users]


@router.get(
    "/{id}",
    response_model=types.User,
    dependencies=[Depends(get_user())],
    response_model_exclude={"email", "email_token", "email_verified", "password"},
    responses=user_auth_responses | {
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.UserNotFound
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


@router.get(
    "/email/verify/{id}",
    response_model=types.User,
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
        user: types.User = Depends(
            get_user(check_email_verified=False)
        )
):
    if user.email_verified:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Email already confirmed"
        )

    if user.email_token != id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Email token is incorrect"
        )

    verified_user = await holder.user.verify_email(user_id=user.id)

    if not verified_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Authentication user not found"
        )

    return types.User.from_dto(user=verified_user)


@router.post(
    "/",
    response_model=types.User,
    response_model_exclude={"password", "email_token"},
    responses={
        HTTP_409_CONFLICT: {"model": Union[responses.EmailAlreadyExists, responses.UsernameAlreadyExists]},
        HTTP_400_BAD_REQUEST: {"description": "Unable to create user error", "model": responses.UnableCreateUser}
    }
)
async def create(
        user_create: types.UserCreate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        crypt_context: CryptContext = Depends(CryptContextMarker),
        js: JetStreamContext = Depends(NatsJetStreamMarker),
        settings: types.Settings = Depends(SettingsMarker)
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

    email_broadcaster = types.EmailBroadcast(
        to_address=user_create.email,
        subject="Confirm email",
        html=f"To activate the user account, follow the link {settings.email_verify_url}/{user.email_token}"
    )

    await js.publish(
        subject=f"{settings.nats_stream_name}.broadcast.email.{str(user.id)}",
        payload=msgpack.packb(dict(json.loads(email_broadcaster.json()))),
        stream=settings.nats_stream_name
    )

    return types.User.from_dto(user=user)
