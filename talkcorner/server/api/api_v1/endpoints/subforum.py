from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.common import types
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.core.auth import get_user

router = APIRouter()


@router.get(
    "/",
    response_model=list[types.Subforum],
    dependencies=[Depends(get_user)]
)
async def read_all(
        offset: int = 0,
        limit: int = 5,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    subforums = await holder.subforum.read_all(offset=offset, limit=limit)

    return [types.Subforum.from_dto(subforum=subforum) for subforum in subforums]


@router.get(
    "/{id}",
    response_model=types.Subforum,
    dependencies=[Depends(get_user)]
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    subforum = await holder.subforum.read_by_id(subforum_id=id)

    if not subforum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Subforum not found"
        )

    return types.Subforum.from_dto(subforum=subforum)


@router.post(
    "/",
    response_model=types.Subforum
)
async def create(
        subforum_create: types.SubforumCreate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    parent_forum = await holder.forum.read_by_id(forum_id=subforum_create.parent_forum_id)

    if not parent_forum or parent_forum.creator_id != user.id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Parent forum not found or you cannot interact with this forum"
        )

    child_forum = await holder.forum.read_by_id(forum_id=subforum_create.child_forum_id)

    if not child_forum or child_forum.creator_id != user.id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Child forum not found or you cannot interact with this forum"
        )

    subforum = await holder.subforum.create(
        parent_forum_id=subforum_create.parent_forum_id,
        child_forum_id=subforum_create.child_forum_id,
        creator_id=user.id
    )

    if not subforum:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unable to create subforum"
        )

    return types.Subforum.from_dto(subforum=subforum)


@router.put(
    "/{id}",
    response_model=types.Subforum
)
async def update(
        id: int,
        subforum_update: types.SubforumUpdate,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    if subforum_update.parent_forum_id:
        parent_forum = await holder.forum.read_by_id(forum_id=subforum_update.parent_forum_id)

        if not parent_forum or parent_forum.creator_id != user.id:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Parent forum not found or you cannot interact with this forum"
            )

    if subforum_update.child_forum_id:
        child_forum = await holder.forum.read_by_id(forum_id=subforum_update.child_forum_id)

        if not child_forum or child_forum.creator_id != user.id:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Child forum not found or you cannot interact with this forum"
            )

    subforum = await holder.subforum.update(
        subforum_id=id,
        creator_id=user.id,
        data=subforum_update.dict(exclude_unset=True)
    )

    if not subforum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Subforum not found or you cannot update this subforum"
        )

    return types.Subforum.from_dto(subforum=subforum)


@router.delete(
    "/{id}",
    response_model=types.Subforum
)
async def delete(
        id: int,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        user: types.User = Depends(get_user)
):
    subforum = await holder.subforum.delete(subforum_id=id, creator_id=user.id)

    if not subforum:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Subforum not found or you cannot delete this subforum"
        )

    return types.Subforum.from_dto(subforum=subforum)
