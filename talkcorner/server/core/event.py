from typing import Callable, Coroutine, Any

import nats
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from talkcorner.server.api.api_v1.dependencies.database import DatabaseEngineMarker
from talkcorner.server.api.api_v1.dependencies.nats import NatsMarker
from talkcorner.common import types
from talkcorner.common.queue.nats.factory import (
    nats_create_connect,
    nats_create_jetstream,
    js_create_or_update_stream
)


def create_on_startup_handler(
        app: FastAPI,
        settings: types.Setting,
        **kwargs: Any
) -> Callable[..., Coroutine[Any, Any, None]]:

    async def on_startup() -> None:
        nats = await nats_create_connect(connection_uri=settings.NATS_URL)
        js = nats_create_jetstream(nats=nats)
        await js_create_or_update_stream(js=js, stream_name=settings.NATS_STREAM_NAME)

        app.dependency_overrides.update(
            {
                NatsMarker: lambda: nats
            }
        )

    return on_startup


def create_on_shutdown_handler(app: FastAPI) -> Callable[..., Coroutine[Any, Any, None]]:

    async def on_shutdown() -> None:
        engine: AsyncEngine = app.dependency_overrides[DatabaseEngineMarker]()
        nc: nats.NATS = app.dependency_overrides[NatsMarker]()

        await engine.dispose()
        await nc.close()

    return on_shutdown
