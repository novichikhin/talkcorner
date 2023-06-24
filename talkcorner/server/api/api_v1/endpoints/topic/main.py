import uuid
from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from talkcorner.common import types, exceptions
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.common.types import errors
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.core.auth import get_user

router = APIRouter(
    responses={
        HTTP_401_UNAUTHORIZED: {"description": "Could not validate credentials error", "model": errors.Credentials},
        HTTP_404_NOT_FOUND: {"description": "User not found error", "model": errors.AuthenticationUserNotFound}
    }
)


@router.get(
    "/",
    response_model=list[types.Topic],
    dependencies=[Depends(get_user)]
)
async def read_all(
        offset: int = 0,
        limit: int = 5,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    topics = await holder.topic.read_all(offset=offset, limit=limit)

    return [types.Topic.from_dto(topic=topic) for topic in topics]


@router.get(
    "/{id}",
    response_model=types.Topic,
    dependencies=[Depends(get_user)],
    responses={
        HTTP_404_NOT_FOUND: {"model": Union[errors.AuthenticationUserNotFound, errors.TopicNotFound]}
    }
)
async def read(id: uuid.UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    topic = await holder.topic.read_by_id(topic_id=id)

    if not topic:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    return types.Topic.from_dto(topic=topic)


@router.post(
    "/",
    response_model=types.Topic,
    responses={
        HTTP_404_NOT_FOUND: {"model": Union[errors.AuthenticationUserNotFound, errors.ForumNotFound]},
        HTTP_400_BAD_REQUEST: {"description": "Unable to create topic error", "model": errors.UnableCreateTopic}
    }
)
async def create(
        topic_create: types.TopicCreate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    try:
        topic = await holder.topic.create(
            forum_id=topic_create.forum_id,
            title=topic_create.title,
            body=topic_create.body,
            creator_id=user.id
        )
    except exceptions.ForumNotFound:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Forum not found"
        )
    except exceptions.UnableInteraction:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to create topic"
        )

    return types.Topic.from_dto(topic=topic)


@router.put(
    "/{id}",
    response_model=types.Topic,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": Union[
                errors.AuthenticationUserNotFound,
                errors.ForumNotFound,
                errors.TopicNotFoundOrNotCreator
            ]
        },
        HTTP_400_BAD_REQUEST: {"description": "Unable to update topic error", "model": errors.UnableUpdateTopic}
    }
)
async def update(
        id: uuid.UUID,
        topic_update: types.TopicUpdate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    try:
        topic = await holder.topic.update(
            topic_id=id,
            creator_id=user.id,
            data=topic_update.dict(exclude_unset=True)
        )
    except exceptions.ForumNotFound:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Forum not found"
        )
    except exceptions.UnableInteraction:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to update topic"
        )

    if not topic:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Topic not found or you are not the creator of this topic"
        )

    return types.Topic.from_dto(topic=topic)


@router.delete(
    "/{id}",
    response_model=types.Topic,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": Union[
                errors.AuthenticationUserNotFound,
                errors.TopicNotFoundOrNotCreator
            ]
        }
    }
)
async def delete(
        id: uuid.UUID,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    topic = await holder.topic.delete(topic_id=id, creator_id=user.id)

    if not topic:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Topic not found or you are not the creator of this topic"
        )

    return types.Topic.from_dto(topic=topic)
