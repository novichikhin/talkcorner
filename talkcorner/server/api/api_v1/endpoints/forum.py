from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.common import types, exceptions
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.server.api.api_v1 import responses
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.responses.main import user_auth_responses
from talkcorner.server.core.auth import get_user

router = APIRouter(responses=user_auth_responses)


@router.get(
    "/",
    response_model=list[types.Forum],
    dependencies=[Depends(get_user())]
)
async def read_all(
        offset: int = Query(default=0, ge=0, le=500),
        limit: int = Query(default=5, ge=1, le=1000),
        holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    forums = await holder.forum.read_all(offset=offset, limit=limit)

    return [types.Forum.from_dto(forum=forum) for forum in forums]


@router.get(
    "/{id}",
    response_model=types.Forum,
    dependencies=[Depends(get_user())],
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.ForumNotFound
        }
    }
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    forum = await holder.forum.read_by_id(forum_id=id)

    if not forum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Forum not found"
        )

    return types.Forum.from_dto(forum=forum)


@router.post(
    "/",
    response_model=types.Forum
)
async def create(
        forum_create: types.ForumCreate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user())
):
    forum = await holder.forum.create(
        title=forum_create.title,
        description=forum_create.description,
        creator_id=user.id
    )

    return types.Forum.from_dto(forum=forum)


@router.put(
    "/{id}",
    response_model=types.Forum,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Unable to update forum error",
            "model": responses.UnableUpdateForum
        },
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.ForumNotFoundOrNotCreator
        }
    }
)
async def update(
        id: int,
        forum_update: types.ForumUpdate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user())
):
    try:
        forum = await holder.forum.update(
            forum_id=id,
            creator_id=user.id,
            data=forum_update.dict(exclude_unset=True)
        )
    except exceptions.UnableInteraction:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to update forum"
        )

    if not forum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Forum not found or you are not the creator of this forum"
        )

    return types.Forum.from_dto(forum=forum)


@router.delete(
    "/{id}",
    response_model=types.Forum,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.ForumNotFoundOrNotCreator
        }
    }
)
async def delete(
        id: int,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user())
):
    forum = await holder.forum.delete(forum_id=id, creator_id=user.id)

    if not forum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Forum not found or you are not the creator of this forum"
        )

    return types.Forum.from_dto(forum=forum)
