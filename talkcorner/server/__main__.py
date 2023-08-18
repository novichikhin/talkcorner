import logging
import asyncio

import uvicorn

from talkcorner.common.settings.app import AppSettings
from talkcorner.server.api.setup import register_app


def run_application() -> None:
    settings = AppSettings()
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
