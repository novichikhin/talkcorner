import uuid

from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from passlib.context import CryptContext

from talkcorner.settings.environments.app import AppSettings
from talkcorner.exceptions.user import (
    WrongUsernameOrPasswordError,
    EmailNotActivatedError,
    NotValidateCredentialsError,
)
from talkcorner.database.holder import DatabaseHolder
from talkcorner.enums.credential import CredentialType

from talkcorner.schemas.user import User
from talkcorner.services.auth.security import verify_password


def get_token(authorization: str) -> str:
    scheme, _, param = authorization.partition(" ")

    if scheme.lower() != "bearer":
        raise NotValidateCredentialsError

    return param


async def authorize_user(
    username: str, password: str, holder: DatabaseHolder, crypt_context: CryptContext
) -> User:
    user = await holder.user.read_by_login(username=username)

    if not verify_password(
        crypt_context=crypt_context,
        plain_password=password,
        hashed_password=user.password,
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
            algorithms=[ALGORITHMS.HS256],
        )
    except JWTError:
        raise NotValidateCredentialsError

    user_id = payload.get("user_id")

    if not user_id:
        raise NotValidateCredentialsError

    try:
        user_id = uuid.UUID(hex=user_id)
    except ValueError:
        raise NotValidateCredentialsError

    user = await holder.user.read_by_authenticate(user_id=user_id)

    if check_email_verified and not user.email_verified:
        raise EmailNotActivatedError

    return user
