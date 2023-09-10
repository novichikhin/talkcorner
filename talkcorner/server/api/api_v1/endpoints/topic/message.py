import uuid
from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.server.api.api_v1 import responses
from talkcorner.server.api.api_v1.core.auth import api_authenticate_user
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.responses.main import user_auth_responses
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.topic.message import TopicMessage, TopicMessageCreate, TopicMessagePatch
from talkcorner.server.schemas.user import User
from talkcorner.server.services.topic.message import (
    get_topic_messages,
    get_topic_message,
    create_topic_message,
    patch_topic_message,
    delete_topic_message
)

router = APIRouter(responses=user_auth_responses)


@router.get(
    "/",
    response_model=List[TopicMessage],
    dependencies=[Depends(api_authenticate_user())]
)
async def read_all(
    offset: int = Query(default=0, ge=0, le=500),
    limit: int = Query(default=5, ge=1, le=1000),
    holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    return await get_topic_messages(
        offset=offset,
        limit=limit,
        holder=holder
    )


@router.get(
    "/{id}",
    response_model=TopicMessage,
    dependencies=[Depends(api_authenticate_user())],
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.TopicMessageNotFound
        }
    }
)
async def read(id: uuid.UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_topic_message(topic_message_id=id, holder=holder)


@router.post(
    "/",
    response_model=TopicMessage,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.TopicNotFound
        }
    }
)
async def create(
    topic_message_create: TopicMessageCreate,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user())
):
    return await create_topic_message(
        topic_message_create=topic_message_create,
        holder=holder,
        user=user
    )


@router.patch(
    "/{id}",
    response_model=TopicMessage,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Topic message not updated error",
            "model": responses.TopicMessageNotUpdated
        }
    }
)
async def patch(
    id: uuid.UUID,
    topic_message_patch: TopicMessagePatch,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user())
):
    return await patch_topic_message(
        topic_message_id=id,
        topic_message_patch=topic_message_patch,
        holder=holder,
        user=user
    )


@router.delete(
    "/{id}",
    response_model=TopicMessage,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Topic message not deleted error",
            "model": responses.TopicMessageNotDeleted
        }
    }
)
async def delete(
    id: uuid.UUID,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user())
):
    return await delete_topic_message(
        topic_message_id=id,
        holder=holder,
        user=user
    )
