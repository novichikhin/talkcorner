from fastapi import FastAPI, APIRouter

from talkcorner.common import types
from talkcorner.server.api.api_v1.endpoints import (
    user,
    forum,
    subforum
)


def register_routers(app: FastAPI, settings: types.Setting) -> None:
    router = APIRouter()

    router.include_router(
        user.router,
        prefix="/user",
        tags=["user"]
    )

    router.include_router(
        forum.router,
        prefix="/forum",
        tags=["forum"]
    )

    router.include_router(
        subforum.router,
        prefix="/subforum",
        tags=["subforum"]
    )

    app.include_router(router=router, prefix=settings.api_v1_str)
