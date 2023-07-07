from talkcorner.common.types.errors.common import Error

class NotValidateCredentials(Error):
    detail: str = "Could not validate credentials"


class AuthenticationUserNotFound(Error):
    detail: str = "Authentication user not found"


class UserNotFound(Error):
    detail: str = "User not found"


class WrongUsernameOrPassword(Error):
    detail: str = "Wrong username (email) or password"


class EmailAlreadyConfirmed(Error):
    detail: str = "Email already confirmed"


class EmailTokenIncorrect(Error):
    detail: str = "Email token is incorrect"


class EmailAlreadyExists(Error):
    detail: str = "User email already exists"


class UsernameAlreadyExists(Error):
    detail: str = "User username already exists"


class UnableCreateUser(Error):
    detail: str = "Unable to create user"
