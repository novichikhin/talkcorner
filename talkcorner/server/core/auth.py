import uuid
from typing import Callable, Awaitable

from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from talkcorner.common import types
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.core.security import verify_password

credentials_exception = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)


def get_token(authorization: str) -> str:
    scheme, _, param = authorization.partition(" ")

    if scheme.lower() != "bearer":
        raise credentials_exception

    return param


async def verify_refresh_token(
        authorization: str = Header(alias="Authorization"),
        settings: types.Setting = Depends(SettingsMarker)
) -> types.RefreshToken:
    refresh_token = get_token(authorization=authorization)

    try:
        payload = jwt.decode(
            token=refresh_token,
            key=settings.authorize_refresh_token_secret_key,
            algorithms=[ALGORITHMS.HS256]
        )

        if not (user_id := payload.get("user_id")):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return types.RefreshToken(token=refresh_token, user_id=uuid.UUID(user_id))


async def authenticate_user(
        username: str,
        password: str,
        holder: DatabaseHolder,
        crypt_context: CryptContext
) -> types.User:
    user = await holder.user.read_by_login(username=username)

    if not user or not verify_password(
            crypt_context=crypt_context,
            plain_password=password,
            hashed_password=user.password
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Wrong username (email) or password"
        )

    return types.User.from_dto(user=user)


def get_user(
        check_email_verified: bool = True
) -> Callable[[str, DatabaseHolder, types.Setting], Awaitable[types.User]]:

    async def wrapper(
            authorization: str = Header(alias="Authorization"),
            holder: DatabaseHolder = Depends(DatabaseHolderMarker),
            settings: types.Setting = Depends(SettingsMarker)
    ) -> types.User:
        try:
            payload = jwt.decode(
                token=get_token(authorization=authorization),
                key=settings.authorize_access_token_secret_key,
                algorithms=[ALGORITHMS.HS256]
            )

            user_id = payload.get("user_id")

            if not user_id:
                raise credentials_exception

            try:
                user_id = uuid.UUID(hex=user_id)
            except ValueError:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = await holder.user.read_by_id(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Authentication user not found"
            )

        if check_email_verified and not user.email_verified:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Email is not activated"
            )

        return types.User.from_dto(user=user)

    return wrapper
