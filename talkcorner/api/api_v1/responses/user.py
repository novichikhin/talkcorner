import uuid

from pydantic import BaseModel

from talkcorner.api.api_v1.responses.base import BaseResponse
from talkcorner.enums.credential import CredentialType


class NotValidateCredentialsDetail(BaseModel):
    message: str = "Could not validate credentials"
    credential: CredentialType


class NotValidateCredentials(BaseResponse):
    detail: NotValidateCredentialsDetail


class UserNotFoundDetail(BaseModel):
    message: str = "User not found"
    user_id: uuid.UUID


class UserNotFound(BaseResponse):
    detail: UserNotFoundDetail


class AuthenticationUserNotFoundDetail(BaseModel):
    message: str = "Authentication user not found"
    user_id: uuid.UUID


class AuthenticationUserNotFound(BaseResponse):
    detail: AuthenticationUserNotFoundDetail


class UsernameAlreadyExists(BaseResponse):
    detail: str = "Username already exists"


class EmailAlreadyExists(BaseResponse):
    detail: str = "Email already exists"


class EmailAlreadyConfirmed(BaseResponse):
    detail: str = "Email already confirmed"


class EmailTokenIncorrect(BaseResponse):
    detail: str = "Email token is incorrect"


class WrongUsernameOrPassword(BaseResponse):
    detail: str = "Wrong username or password"


class EmailNotActivated(BaseResponse):
    detail: str = "Email is not activated"


class EmailNotVerified(BaseResponse):
    detail: str = "Email is not verified"
