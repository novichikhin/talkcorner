from typing import Union, List

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from talkcorner.server.api.api_v1 import responses
from talkcorner.server.api.api_v1.core.auth import api_get_user
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.responses.main import user_auth_responses
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.subforum import Subforum, SubforumCreate, SubforumUpdate
from talkcorner.server.schemas.user import User
from talkcorner.server.services.subforum import (
    get_subforums,
    get_subforum,
    create_subforum,
    update_subforum,
    delete_subforum
)

router = APIRouter(responses=user_auth_responses)


@router.get(
    "/",
    response_model=List[Subforum],
    dependencies=[Depends(api_get_user())]
)
async def read_all(
    offset: int = Query(default=0, ge=0, le=500),
    limit: int = Query(default=5, ge=1, le=1000),
    holder: DatabaseHolder = Depends(DatabaseHolderMarker)
):
    return await get_subforums(
        offset=offset,
        limit=limit,
        holder=holder
    )


@router.get(
    "/{id}",
    response_model=Subforum,
    dependencies=[Depends(api_get_user())],
    responses={
        HTTP_404_NOT_FOUND: {
            "model": user_auth_responses[HTTP_404_NOT_FOUND]["model"] | responses.SubforumNotFound
        }
    }
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_subforum(subforum_id=id, holder=holder)


@router.post(
    "/",
    response_model=Subforum,
    responses={
        HTTP_400_BAD_REQUEST: {
            "model": Union[
                responses.ForumNotCreator,
                responses.ParentChildForumsAlreadyExists
            ]
        }
    }
)
async def create(
    subforum_create: SubforumCreate,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_get_user())
):
    return await create_subforum(
        subforum_create=subforum_create,
        holder=holder,
        user=user
    )


@router.put(
    "/{id}",
    response_model=Subforum,
    responses={
        HTTP_400_BAD_REQUEST: {
            "model": Union[
                responses.ForumNotCreator,
                responses.ParentChildForumsAlreadyExists,
                responses.SubforumNotUpdated
            ]
        }
    }
)
async def update(
    id: int,
    subforum_update: SubforumUpdate,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_get_user())
):
    return await update_subforum(
        subforum_id=id,
        subforum_update=subforum_update,
        holder=holder,
        user=user
    )


@router.delete(
    "/{id}",
    response_model=Subforum,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": "Subforum not deleted error",
            "model": responses.SubforumNotDeleted
        }
    }
)
async def delete(
    id: int,
    holder: DatabaseHolder = Depends(DatabaseHolderMarker),
    user: User = Depends(api_get_user())
):
    return await delete_subforum(
        subforum_id=id,
        holder=holder,
        user=user
    )
