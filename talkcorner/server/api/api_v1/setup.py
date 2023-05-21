from fastapi import FastAPI, APIRouter

from talkcorner.server import types


def register_routers(app: FastAPI, settings: types.Setting) -> None:
    router = APIRouter()

    app.include_router(router=router, prefix=settings.API_V1_STR)
