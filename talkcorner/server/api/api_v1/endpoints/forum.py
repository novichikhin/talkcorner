from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.common import types
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.core.auth import get_user

router = APIRouter()


@router.get(
    "/",
    response_model=list[types.Forum],
    dependencies=[Depends(get_user)]
)
async def read_all(
        offset: int = 0,
        limit: int = 5,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    forums = await holder.forum.read_all(offset=offset, limit=limit)

    return [types.Forum.from_dto(forum=forum) for forum in forums]


@router.get(
    "/{id}",
    response_model=types.Forum,
    dependencies=[Depends(get_user)]
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
        user: types.User = Depends(get_user)
):
    forum = await holder.forum.create(
        title=forum_create.title,
        description=forum_create.description,
        creator_id=user.id
    )

    if not forum:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to create forum"
        )

    return types.Forum.from_dto(forum=forum)


@router.put(
    "/{id}",
    response_model=types.Forum
)
async def update(
        id: int,
        forum_update: types.ForumUpdate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    forum = await holder.forum.update(
        forum_id=id,
        creator_id=user.id,
        data=forum_update.dict(exclude_unset=True)
    )

    if not forum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Forum not found or you cannot update this forum"
        )

    return types.Forum.from_dto(forum=forum)


@router.delete(
    "/{id}",
    response_model=types.Forum
)
async def delete(
        id: int,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    forum = await holder.forum.delete(forum_id=id, creator_id=user.id)

    if not forum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Forum not found or you cannot delete this forum"
        )

    return types.Forum.from_dto(forum=forum)
