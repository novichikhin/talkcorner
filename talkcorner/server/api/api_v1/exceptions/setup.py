from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST
)

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException
from talkcorner.server.api.api_v1.exceptions.forum import (
    ForumNotFoundError,
    ForumNotCreatorError,
    ForumNotPatchedError,
    ForumNotDeletedError
)
from talkcorner.server.api.api_v1.exceptions.subforum import (
    SubforumNotFoundError,
    SubforumNotPatchedError,
    SubforumNotDeletedError,
    ParentChildForumsAlreadyExistsError
)
from talkcorner.server.api.api_v1.exceptions.topic.main import (
    TopicNotFoundError,
    TopicNotPatchedError,
    TopicNotDeletedError
)
from talkcorner.server.api.api_v1.exceptions.topic.message import (
    TopicMessageNotFoundError,
    TopicMessageNotPatchedError,
    TopicMessageNotDeletedError
)
from talkcorner.server.api.api_v1.exceptions.user import (
    NotValidateCredentialsError,
    UserNotFoundError,
    AuthenticationUserNotFoundError,
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    EmailAlreadyConfirmedError,
    EmailTokenIncorrectError,
    WrongUsernameOrPasswordError,
    EmailNotActivatedError,
    EmailNotVerifiedError
)


def init_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(
        NotValidateCredentialsError,
        not_validate_credentials_error_handler
    )
    app.add_exception_handler(
        UserNotFoundError,
        user_not_found_error_handler
    )
    app.add_exception_handler(
        AuthenticationUserNotFoundError,
        authentication_user_not_found_error_handler
    )
    app.add_exception_handler(
        UsernameAlreadyExistsError,
        username_already_exists_error_handler
    )
    app.add_exception_handler(
        EmailAlreadyExistsError,
        email_already_exists_error_handler
    )
    app.add_exception_handler(
        EmailAlreadyConfirmedError,
        email_already_confirmed_error_handler
    )
    app.add_exception_handler(
        EmailTokenIncorrectError,
        email_token_incorrect_error_handler
    )
    app.add_exception_handler(
        WrongUsernameOrPasswordError,
        wrong_username_or_password_error_handler
    )
    app.add_exception_handler(
        EmailNotActivatedError,
        email_not_activated_error_handler
    )
    app.add_exception_handler(
        EmailNotVerifiedError,
        email_not_verified_error_handler
    )

    app.add_exception_handler(
        ForumNotFoundError,
        forum_not_found_error_handler
    )
    app.add_exception_handler(
        ForumNotCreatorError,
        forum_not_creator_error_handler
    )
    app.add_exception_handler(
        ForumNotPatchedError,
        forum_not_updated_error_handler
    )
    app.add_exception_handler(
        ForumNotDeletedError,
        forum_not_deleted_error_handler
    )

    app.add_exception_handler(
        SubforumNotFoundError,
        subforum_not_found_error_handler
    )
    app.add_exception_handler(
        SubforumNotPatchedError,
        subforum_not_updated_error_handler
    )
    app.add_exception_handler(
        SubforumNotDeletedError,
        subforum_not_deleted_error_handler
    )
    app.add_exception_handler(
        ParentChildForumsAlreadyExistsError,
        parent_child_forums_already_exists_error
    )

    app.add_exception_handler(
        TopicNotFoundError,
        topic_not_found_error_handler
    )
    app.add_exception_handler(
        TopicNotPatchedError,
        topic_not_updated_error_handler
    )
    app.add_exception_handler(
        TopicNotDeletedError,
        topic_not_deleted_error_handler
    )

    app.add_exception_handler(
        TopicMessageNotFoundError,
        topic_message_not_found_error_handler
    )
    app.add_exception_handler(
        TopicMessageNotPatchedError,
        topic_message_not_updated_error_handler
    )
    app.add_exception_handler(
        TopicMessageNotDeletedError,
        topic_message_not_deleted_error_handler
    )

    app.add_exception_handler(
        RequestValidationError,
        request_validation_error_handler
    )
    app.add_exception_handler(Exception, exception_handler)


def not_validate_credentials_error_handler(
    _,
    e: NotValidateCredentialsError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_401_UNAUTHORIZED)


def user_not_found_error_handler(
    _,
    e: UserNotFoundError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_404_NOT_FOUND)


def authentication_user_not_found_error_handler(
    _,
    e: AuthenticationUserNotFoundError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_404_NOT_FOUND)


def username_already_exists_error_handler(
    _,
    e: UsernameAlreadyExistsError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_409_CONFLICT)


def email_already_exists_error_handler(
    _,
    e: EmailAlreadyExistsError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_409_CONFLICT)


def email_already_confirmed_error_handler(
    _,
    e: EmailAlreadyConfirmedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_403_FORBIDDEN)


def email_token_incorrect_error_handler(
    _,
    e: EmailTokenIncorrectError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_403_FORBIDDEN)


def wrong_username_or_password_error_handler(
    _,
    e: WrongUsernameOrPasswordError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_401_UNAUTHORIZED)


def email_not_activated_error_handler(
    _,
    e: EmailNotActivatedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_403_FORBIDDEN)


def email_not_verified_error_handler(
    _,
    e: EmailNotVerifiedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_403_FORBIDDEN)


def forum_not_found_error_handler(
    _,
    e: ForumNotFoundError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_404_NOT_FOUND)


def forum_not_creator_error_handler(
    _,
    e: ForumNotCreatorError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def forum_not_updated_error_handler(
    _,
    e: ForumNotPatchedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def forum_not_deleted_error_handler(
    _,
    e: ForumNotDeletedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def subforum_not_found_error_handler(
    _,
    e: SubforumNotFoundError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_404_NOT_FOUND)


def subforum_not_updated_error_handler(
    _,
    e: SubforumNotPatchedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def subforum_not_deleted_error_handler(
    _,
    e: SubforumNotDeletedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def parent_child_forums_already_exists_error(
    _,
    e: ParentChildForumsAlreadyExistsError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def topic_not_found_error_handler(
    _,
    e: TopicNotFoundError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_404_NOT_FOUND)


def topic_not_updated_error_handler(
    _,
    e: TopicNotPatchedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def topic_not_deleted_error_handler(
    _,
    e: TopicNotDeletedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def topic_message_not_found_error_handler(
    _,
    e: TopicMessageNotFoundError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_404_NOT_FOUND)


def topic_message_not_updated_error_handler(
    _,
    e: TopicMessageNotPatchedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def topic_message_not_deleted_error_handler(
    _,
    e: TopicMessageNotDeletedError
) -> JSONResponse:
    return handle_error(err=e, status_code=HTTP_400_BAD_REQUEST)


def request_validation_error_handler(
    _,
    e: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        {"detail": e.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


def exception_handler(_, e: Exception) -> JSONResponse:
    return JSONResponse(
        {"detail": "Something went wrong"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR
    )


def handle_error(
    err: BaseAppException,
    status_code: int
) -> JSONResponse:
    return JSONResponse({"detail": err.detail}, status_code=status_code)
