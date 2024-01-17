import uuid
from dataclasses import dataclass
from typing import Union, Dict, Any

from talkcorner.exceptions.base import BaseAppException


@dataclass(frozen=True)
class NotValidateCredentialsError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Could not validate credentials"


@dataclass(frozen=True)
class UserNotFoundError(BaseAppException):
    user_id: uuid.UUID

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return {
            "message": "User not found",
            "user_id": self.user_id
        }


@dataclass(frozen=True)
class AuthenticationUserNotFoundError(BaseAppException):
    user_id: uuid.UUID

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return {
            "message": "Authentication user not found",
            "user_id": self.user_id
        }


class UsernameAlreadyExistsError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Username already exists"


class EmailAlreadyExistsError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Email already exists"


class EmailAlreadyConfirmedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Email already confirmed"


class EmailTokenIncorrectError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Email token is incorrect"


class WrongUsernameOrPasswordError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Wrong username or password"


class EmailNotActivatedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Email is not activated"


class EmailNotVerifiedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Email is not verified"
