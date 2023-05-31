from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from passlib.context import CryptContext

from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker, DatabaseEngineMarker
from talkcorner.server.api.api_v1.dependencies.security import CryptContextMarker
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.api.api_v1.endpoints.setup import register_routers
from talkcorner.server.core.event import create_on_startup_handler, create_on_shutdown_handler
from talkcorner.common import types
from talkcorner.common.database.factory import (
    sa_create_engine,
    sa_create_session_factory,
    sa_create_holder
)
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
        }
    )

    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    engine = sa_create_engine(connection_uri=settings.database_uri)
    session_factory = sa_create_session_factory(engine=engine)

    register_routers(app=app, settings=settings)

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings,
            DatabaseEngineMarker: lambda: engine,
            DatabaseHolderMarker: sa_create_holder(session_factory=session_factory),
            CryptContextMarker: lambda: crypt_context
        }
    )

    app.add_event_handler("startup", create_on_startup_handler(app, settings))
    app.add_event_handler("shutdown", create_on_shutdown_handler(app))

    return app
