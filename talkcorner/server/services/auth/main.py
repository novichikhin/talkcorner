import uuid

from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from passlib.context import CryptContext

from talkcorner.common.settings.environments.app import AppSettings
from talkcorner.server.api.api_v1.exceptions.user import (
    WrongUsernameOrPasswordError,
    EmailNotActivatedError,
    NotValidateCredentialsError
)
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.enums.credential import CredentialType

from talkcorner.server.schemas.user import User
from talkcorner.server.services.auth.security import verify_password


def get_token(authorization: str) -> str:
    scheme, _, param = authorization.partition(" ")

    if scheme.lower() != "bearer":
        raise NotValidateCredentialsError(credential=CredentialType.AUTHORIZATION_NOT_BEARER)

    return param


async def authorize_user(
    username: str,
    password: str,
    holder: DatabaseHolder,
    crypt_context: CryptContext
) -> User:
    user = await holder.user.read_by_login(username=username)

    if not verify_password(
        crypt_context=crypt_context,
        plain_password=password,
        hashed_password=user.password
    ):
        raise WrongUsernameOrPasswordError

    return user


async def authenticate_user(
    *,
    authorization: str,
    check_email_verified: bool,
    holder: DatabaseHolder,
    settings: AppSettings
) -> User:
    try:
        payload = jwt.decode(
            token=get_token(authorization=authorization),
            key=settings.authorize_access_token_secret_key,
            algorithms=[ALGORITHMS.HS256]
        )
    except JWTError:
        raise NotValidateCredentialsError(credential=CredentialType.JWT_ERROR)

    user_id = payload.get("user_id")

    if not user_id:
        raise NotValidateCredentialsError(credential=CredentialType.JWT_PAYLOAD)

    try:
        user_id = uuid.UUID(hex=user_id)
    except ValueError:
        raise NotValidateCredentialsError(credential=CredentialType.USER_ID_NOT_UUID)

    user = await holder.user.read_by_authenticate(user_id=user_id)

    if check_email_verified and not user.email_verified:
        raise EmailNotActivatedError

    return user
