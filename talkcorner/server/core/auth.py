import uuid
import datetime as dt

from typing import Any

from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from talkcorner.common import types
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.core.security import verify_password

credentials_exception = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


def get_token(authorization: str) -> str:
    scheme, _, param = authorization.partition(" ")

    if scheme.lower() != "bearer":
        raise credentials_exception

    return param


def create_access_token(payload: dict[str, Any], settings: types.Setting) -> str:
    return jwt.encode(
        claims={
            "exp": dt.datetime.utcnow() + dt.timedelta(minutes=settings.AUTHORIZE_ACCESS_TOKEN_EXPIRE_MINUTES),
            **payload
        },
        key=settings.AUTHORIZE_SECRET_KEY,
        algorithm=ALGORITHMS.HS256
    )


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


async def get_user(
        authorization: str = Header(alias="Authorization"),
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        settings: types.Setting = Depends(SettingsMarker)
) -> types.User:
    try:
        payload = jwt.decode(
            token=get_token(authorization=authorization),
            key=settings.AUTHORIZE_SECRET_KEY,
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
            detail=f"User with id {user_id} not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return types.User.from_dto(user=user)