from fastapi import APIRouter

from talkcorner.api.api_v1.endpoints.topic import message
from talkcorner.api.api_v1.endpoints.topic import main


def register_topic_routers() -> APIRouter:
    router = APIRouter()

    router.include_router(main.router, tags=["topic"])

    router.include_router(message.router, prefix="/message", tags=["message"])

    return router
