from fastapi import APIRouter

from talkcorner.api.api_v1.endpoints import (
    forum,
    subforum,
    healthcheck
)
from talkcorner.api.api_v1.endpoints import user
from talkcorner.api.api_v1.endpoints.topic.setup import register_topic_routers


def register_routers() -> APIRouter:
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

    router.include_router(
        healthcheck.router,
        prefix="/healthcheck",
        tags=["healthcheck"]
    )

    router.include_router(
        register_topic_routers(),
        prefix="/topic",
        tags=["topic"]
    )

    return router
