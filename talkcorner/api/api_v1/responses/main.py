from typing import Any, Union

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from talkcorner.api.api_v1 import responses

user_auth_responses: dict[Union[int, str], dict[str, Any]] = {
    HTTP_401_UNAUTHORIZED: {
        "description": "Could not validate credentials error",
        "model": responses.NotValidateCredentials
    },
    HTTP_404_NOT_FOUND: {
        "description": "Authentication user not found error",
        "model": responses.AuthenticationUserNotFound
    }
}
