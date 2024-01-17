import logging
import asyncio
import os

import uvicorn

from talkcorner.settings.environments.base import AppEnvTypes
from talkcorner.settings.main import get_app_settings
from talkcorner.api.setup import register_app


def run_application() -> None:
    settings = get_app_settings(
        app_env=AppEnvTypes.prod if os.getenv("IS_PRODUCTION") else AppEnvTypes.dev
    )
    app = register_app(settings=settings)

    config = uvicorn.Config(
        app,
        host=settings.server_host,
        port=settings.server_port,
        log_level=logging.INFO
    )

    server = uvicorn.Server(config)

    asyncio.run(server.serve())


if __name__ == "__main__":
    run_application()
