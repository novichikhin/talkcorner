from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.api.api_v1 import responses
from talkcorner.api.api_v1.core.auth import api_authenticate_user
from talkcorner.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.api.api_v1.responses.main import user_auth_responses
from talkcorner.database.holder import DatabaseHolder
from talkcorner.schemas.forum import Forum, ForumCreate, ForumPatch
from talkcorner.schemas.user import User
from talkcorner.services.forum import (
    get_forums,
    get_forum,
    create_forum,
    patch_forum,
    delete_forum,
)

router = APIRouter(responses=user_auth_responses)


@router.get(
    "/", response_model=List[Forum], dependencies=[Depends(api_authenticate_user())]
)
async def read_all(
    offset: int = Query(default=0, ge=0, le=500),
    limit: int = Query(default=5, ge=1, le=1000),
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
):
    return await get_forums(offset=offset, limit=limit, holder=holder)


@router.get(
    "/{id}",
    response_model=Forum,
    dependencies=[Depends(api_authenticate_user())],
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"]
            | responses.ForumNotFound
        }
    },
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_forum(forum_id=id, holder=holder)


@router.post("/", response_model=Forum)
async def create(
    forum_create: ForumCreate,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user()),
):
    return await create_forum(forum_create=forum_create, holder=holder, user=user)


@router.patch(
    "/{id}",
    response_model=Forum,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Forum not updated error",
            "model": responses.ForumNotUpdated,
        }
    },
)
async def patch(
    id: int,
    forum_patch: ForumPatch,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user()),
):
    return await patch_forum(
        forum_id=id, forum_patch=forum_patch, holder=holder, user=user
    )


@router.delete(
    "/{id}",
    response_model=Forum,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Forum not deleted error",
            "model": responses.ForumNotDeleted,
        }
    },
)
async def delete(
    id: int,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_authenticate_user()),
):
    return await delete_forum(forum_id=id, holder=holder, user=user)
