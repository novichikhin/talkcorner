import logging
from sys import platform
from typing import Optional

from talkcorner.server.api.setup import register_app
from talkcorner.common import types


def run_application() -> None:
    settings = types.Setting()
    app = register_app(settings)

    if platform == "linux":
        import multiprocessing
        from gunicorn.app.base import BaseApplication
        from typing import Any, Dict

        def number_of_workers() -> int:
            return (multiprocessing.cpu_count() * 2) + 1

        class StandaloneApplication(BaseApplication):
            def __init__(self, application: Any, options: Optional[Dict[str, Any]] = None):
                self.options = options or {}
                self.application = application
                super().__init__()

            def load_config(self) -> None:
                config = {
                    key: value
                    for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None
                }
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self) -> Any:
                return self.application

        options = {
            "bind": f"{settings.SERVER_HOST}:{settings.SERVER_PORT}",
            "preload_app": True,
            "workers": number_of_workers(),
            "worker_class": "uvicorn.workers.UvicornWorker",
        }
        StandaloneApplication(app, options).run()

    elif platform in ["win32", "darwin"]:
        import uvicorn
        import asyncio

        config = uvicorn.Config(
            app,
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=True,
            log_level=logging.INFO
        )

        server = uvicorn.Server(config)

        asyncio.run(server.serve())


if __name__ == "__main__":
    run_application()
