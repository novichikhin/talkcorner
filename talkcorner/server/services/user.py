import json
import uuid
from typing import List

import msgpack
from nats.js import JetStreamContext
from passlib.context import CryptContext

from talkcorner.common.settings.environments.app import AppSettings
from talkcorner.common.types.broadcast.email import EmailBroadcast
from talkcorner.server.api.api_v1.exceptions.base import BaseAppException
from talkcorner.server.api.api_v1.exceptions.user import EmailAlreadyConfirmedError, EmailTokenIncorrectError
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.auth import Authentication, RefreshToken, AccessToken
from talkcorner.server.schemas.user import User, UserCreate
from talkcorner.server.services.auth.main import authorize_user
from talkcorner.server.services.auth.security import get_password_hash
from talkcorner.server.services.auth.token import create_access_token, create_refresh_token


async def login_user(
    *,
    username: str,
    password: str,
    holder: DatabaseHolder,
    crypt_context: CryptContext,
    settings: AppSettings
) -> Authentication:
    user = await authorize_user(
        username=username,
        password=password,
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

    return Authentication(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


async def refresh_token_user(
    *,
    refresh_token: RefreshToken,
    settings: AppSettings
) -> AccessToken:
    new_access_token = create_access_token(
        payload={"user_id": str(refresh_token.user_id)},
        secret_key=settings.authorize_access_token_secret_key,
        expire_minutes=settings.authorize_access_token_expire_minutes
    )

    return AccessToken(access_token=new_access_token, token_type="bearer")


async def get_users(
    *,
    offset: int,
    limit: int,
    holder: DatabaseHolder
) -> List[User]:
    return await holder.user.read_all(offset=offset, limit=limit)


async def get_user(
    *,
    user_id: uuid.UUID,
    holder: DatabaseHolder
) -> User:
    return await holder.user.read_by_id(user_id=user_id)


async def verify_email_user(
    *,
    email_token: uuid.UUID,
    holder: DatabaseHolder,
    user: User
) -> User:
    if user.email_verified:
        raise EmailAlreadyConfirmedError

    if user.email_token != email_token:
        raise EmailTokenIncorrectError

    verified_user = await holder.user.verify_email(user_id=user.id)
    await holder.commit()

    return verified_user


async def create_user(
    *,
    user_create: UserCreate,
    holder: DatabaseHolder,
    crypt_context: CryptContext,
    js: JetStreamContext,
    settings: AppSettings
) -> User:
    try:
        user = await holder.user.create(
            username=user_create.username,
            password=get_password_hash(crypt_context=crypt_context, password=user_create.password),
            email=user_create.email
        )
        await holder.commit()
    except BaseAppException as e:
        await holder.rollback()
        raise e

    email_broadcaster = EmailBroadcast(
        to_address=user_create.email,
        subject="Confirm email",
        html=(
            f"To activate the user account, "
            f"follow the link {settings.email_verify_url}/{user.email_token}"
        )
    )

    await js.publish(
        subject=f"{settings.nats_stream_name}.broadcast.email.{str(user.id)}",
        payload=msgpack.packb(dict(json.loads(email_broadcaster.json()))),
        stream=settings.nats_stream_name
    )

    return user
