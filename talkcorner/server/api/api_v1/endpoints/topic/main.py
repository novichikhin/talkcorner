import uuid
from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.server.api.api_v1 import responses
from talkcorner.server.api.api_v1.core.auth import api_authenticate_user
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.responses.main import user_auth_responses
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.topic.main import Topic, TopicCreate, TopicPatch
from talkcorner.server.schemas.user import User
from talkcorner.server.services.topic.main import (
    get_topics,
    get_topic,
    create_topic,
    patch_topic,
    delete_topic
)

router = APIRouter(responses=user_auth_responses)


@router.get(
    "/",
    response_model=List[Topic],
    dependencies=[Depends(api_authenticate_user())]
)
async def read_all(
    offset: int = Query(default=0, ge=0, le=500),
    limit: int = Query(default=5, ge=1, le=1000),
    holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    return await get_topics(
        offset=offset,
        limit=limit,
        holder=holder
    )


@router.get(
    "/{id}",
    response_model=Topic,
    dependencies=[Depends(api_authenticate_user())],
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.TopicNotFound
        }
    }
)
async def read(id: uuid.UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_topic(topic_id=id, holder=holder)


@router.post(
    "/",
    response_model=Topic,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.ForumNotFound
        }
    }
)
async def create(
    topic_create: TopicCreate,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user())
):
    return await create_topic(
        topic_create=topic_create,
        holder=holder,
        user=user
    )


@router.patch(
    "/{id}",
    response_model=Topic,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.ForumNotFound
        },
        HTTP_400_BAD_REQUEST: {
            "description": "Topic not updated error",
            "model": responses.TopicNotUpdated
        }
    }
)
async def patch(
    id: uuid.UUID,
    topic_patch: TopicPatch,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user())
):
    return await patch_topic(
        topic_id=id,
        topic_patch=topic_patch,
        holder=holder,
        user=user
    )


@router.delete(
    "/{id}",
    response_model=Topic,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Topic not deleted error",
            "model": responses.TopicNotDeleted
        }
    }
)
async def delete(
    id: uuid.UUID,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user())
):
    return await delete_topic(
        topic_id=id,
        holder=holder,
        user=user
    )
