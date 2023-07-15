from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from talkcorner.server.api.api_v1.dependencies.database import DatabaseEngineMarker
from talkcorner.server.api.api_v1.dependencies.nats import NatsMarker, NatsJetStreamMarker
from talkcorner.common import types
from talkcorner.common.queue.nats.factory import (
    nats_create_connect,
    nats_create_jetstream,
    js_create_or_update_stream, nats_build_connection_uri
)
from talkcorner.server.api.api_v1.dependencies.setting import SettingsMarker


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: types.Settings = app.dependency_overrides[SettingsMarker]()

    nats = await nats_create_connect(
        connection_uri=nats_build_connection_uri(
            host=settings.nats_host,
            port=settings.nats_client_port,
            user=settings.nats_user,
            password=settings.nats_password
        )
    )
    js = nats_create_jetstream(nats=nats)

    await js_create_or_update_stream(js=js, stream_name=settings.nats_stream_name)

    app.dependency_overrides.update(
        {
            NatsMarker: lambda: nats,
            NatsJetStreamMarker: lambda: js
        }
    )

    yield

    engine: AsyncEngine = app.dependency_overrides[DatabaseEngineMarker]()

    await engine.dispose()
    await nats.close()
