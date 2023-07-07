import uuid

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.common import types, exceptions
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.common.types import errors
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.responses.user import user_auth_responses
from talkcorner.server.core.auth import get_user

router = APIRouter(responses=user_auth_responses)


@router.get(
    "/",
    response_model=list[types.TopicMessage],
    dependencies=[Depends(get_user())]
)
async def read_all(
        offset: int = 0,
        limit: int = 5,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    topic_messages = await holder.topic_message.read_all(offset=offset, limit=limit)

    return [types.TopicMessage.from_dto(topic_message=topic_message) for topic_message in topic_messages]


@router.get(
    "/{id}",
    response_model=types.TopicMessage,
    dependencies=[Depends(get_user())],
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | errors.TopicMessageNotFound
        }
    }
)
async def read(id: uuid.UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    topic_message = await holder.topic_message.read_by_id(topic_message_id=id)

    if not topic_message:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Topic message not found"
        )

    return types.TopicMessage.from_dto(topic_message=topic_message)


@router.post(
    "/",
    response_model=types.TopicMessage,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | errors.TopicNotFound
        },
        HTTP_400_BAD_REQUEST: {
            "description": "Unable to create topic message error",
            "model": errors.UnableCreateTopicMessage
        }
    }
)
async def create(
        topic_message_create: types.TopicMessageCreate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user())
):
    try:
        topic_message = await holder.topic_message.create(
            topic_id=topic_message_create.topic_id,
            body=topic_message_create.body,
            creator_id=user.id
        )
    except exceptions.TopicNotFound:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    except exceptions.UnableInteraction:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to create topic message"
        )

    return types.TopicMessage.from_dto(topic_message=topic_message)


@router.put(
    "/{id}",
    response_model=types.TopicMessage,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Unable to update topic message",
            "model": errors.UnableUpdateTopicMessage
        },
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | errors.TopicMessageNotFoundOrNotCreator
        }
    }
)
async def update(
        id: uuid.UUID,
        topic_message_update: types.TopicMessageUpdate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user())
):
    try:
        topic_message = await holder.topic_message.update(
            topic_message_id=id,
            creator_id=user.id,
            data=topic_message_update.dict(exclude_unset=True)
        )
    except exceptions.UnableInteraction:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to update topic message"
        )

    if not topic_message:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Topic message not found or you are not the creator of this topic message"
        )

    return types.TopicMessage.from_dto(topic_message=topic_message)


@router.delete(
    "/{id}",
    response_model=types.TopicMessage,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | errors.TopicMessageNotFoundOrNotCreator
        }
    }
)
async def delete(
        id: uuid.UUID,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user())
):
    topic_message = await holder.topic_message.delete(topic_message_id=id, creator_id=user.id)

    if not topic_message:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Topic message not found or you are not the creator of this topic message"
        )

    return types.TopicMessage.from_dto(topic_message=topic_message)
