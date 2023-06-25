from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from talkcorner.common.types import errors

user_auth_responses = {
    HTTP_401_UNAUTHORIZED: {
        "description": "Could not validate credentials error",
        "model": errors.NotValidateCredentials
    },
    HTTP_404_NOT_FOUND: {
        "description": "Authentication user not found error",
        "model": errors.AuthenticationUserNotFound
    }
}
