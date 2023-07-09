from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from talkcorner.server.api.api_v1.dependencies.database import DatabaseEngineMarker
from talkcorner.server.api.api_v1.dependencies.nats import NatsMarker, NatsJetStreamMarker
from talkcorner.common import types
from talkcorner.common.queue.nats.factory import (
    nats_create_connect,
    nats_create_jetstream,
    js_create_or_update_stream
)
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: types.Setting = app.dependency_overrides[SettingsMarker]()

    nats = await nats_create_connect(connection_uri=settings.nats_url)
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
