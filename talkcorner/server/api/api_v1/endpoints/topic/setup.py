from fastapi import APIRouter

from talkcorner.server.api.api_v1.endpoints.topic import main, message


def register_topic_routers() -> APIRouter:
    router = APIRouter()

    router.include_router(main.router, tags=["topic"])

    router.include_router(
        message.router,
        prefix="/message",
        tags=["message"]
    )

    return router
