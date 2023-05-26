from fastapi import FastAPI

from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker, DatabaseEngineMarker
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.api.api_v1.endpoints.setup import register_routers
from talkcorner.server.core.event import create_on_startup_handler, create_on_shutdown_handler
from talkcorner.common import types
from talkcorner.common.database.factory import (
    sa_create_engine,
    sa_create_session_factory,
    sa_create_holder
)


def register_app(settings: types.Setting) -> FastAPI:
    app = FastAPI()

    engine = sa_create_engine(connection_uri=settings.DATABASE_URI)
    session_factory = sa_create_session_factory(engine=engine)

    register_routers(app=app, settings=settings)

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings,
            DatabaseEngineMarker: lambda: engine,
            DatabaseHolderMarker: sa_create_holder(session_factory=session_factory)
        }
    )

    app.add_event_handler("startup", create_on_startup_handler(app, settings))
    app.add_event_handler("shutdown", create_on_shutdown_handler(app))

    return app
