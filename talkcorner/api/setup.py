from fastapi import FastAPI
from passlib.context import CryptContext
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from talkcorner.settings.environments.app import AppSettings
from talkcorner.api.api_v1 import responses
from talkcorner.api.api_v1.dependencies.database import (
    DatabaseHolderMarker,
    DatabaseSessionMarker,
    DatabaseEngineMarker,
)
from talkcorner.api.api_v1.dependencies.security import CryptContextMarker
from talkcorner.api.api_v1.dependencies.setting import SettingsMarker
from talkcorner.api.api_v1.endpoints.setup import register_routers
from talkcorner.api.api_v1.exceptions.setup import init_exceptions
from talkcorner.api.event import lifespan
from talkcorner.database.factory import (
    sa_create_engine,
    sa_build_connection_uri,
    sa_create_session_factory,
    sa_create_holder,
)


def register_app(settings: AppSettings) -> FastAPI:
    app = FastAPI(
        responses={
            HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Something went wrong error",
                "model": responses.SomethingWentWrong,
            }
        },
        lifespan=lifespan,
    )

    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    engine = sa_create_engine(
        connection_uri=sa_build_connection_uri(
            driver=settings.pg_driver,
            host=settings.pg_host,
            port=settings.pg_port,
            user=settings.pg_user,
            password=settings.pg_password,
            db=settings.pg_db,
        )
    )
    session_factory = sa_create_session_factory(engine=engine)

    app.include_router(router=register_routers(), prefix=settings.api_v1_str)
    init_exceptions(app=app)

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings,
            DatabaseEngineMarker: lambda: engine,
            DatabaseSessionMarker: lambda: session_factory,
            DatabaseHolderMarker: sa_create_holder(session_factory=session_factory),
            CryptContextMarker: lambda: crypt_context,
        }
    )

    return app
