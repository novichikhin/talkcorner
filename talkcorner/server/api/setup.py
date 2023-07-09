from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from passlib.context import CryptContext
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from talkcorner.common.types import errors
from talkcorner.server.api.api_v1.dependencies.database import (
    DatabaseHolderMarker,
    DatabaseSessionMarker,
    DatabaseEngineMarker
)
from talkcorner.server.api.api_v1.dependencies.security import CryptContextMarker
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.api.api_v1.endpoints.setup import register_routers
from talkcorner.common import types
from talkcorner.common.database.factory import (
    sa_create_engine,
    sa_create_session_factory,
    sa_create_holder
)
from talkcorner.server.core.event import lifespan
from talkcorner.server.core.exceptions.handler import (
    http_exception_handler,
    request_validation_error_handler,
    exception_handler
)


def register_app(settings: types.Setting) -> FastAPI:
    app = FastAPI(
        exception_handlers={
            HTTPException: http_exception_handler,
            RequestValidationError: request_validation_error_handler,
            Exception: exception_handler
        },
        responses={
            HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation error", "model": errors.Validation},
            HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Something went wrong error",
                "model": errors.SomethingWentWrong
            }
        },
        lifespan=lifespan
    )

    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    engine = sa_create_engine(connection_uri=settings.database_uri)
    session_factory = sa_create_session_factory(engine=engine)

    app.include_router(router=register_routers(), prefix=settings.api_v1_str)

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings,
            DatabaseEngineMarker: lambda: engine,
            DatabaseSessionMarker: lambda: session_factory,
            DatabaseHolderMarker: sa_create_holder(session_factory=session_factory),
            CryptContextMarker: lambda: crypt_context
        }
    )

    return app
