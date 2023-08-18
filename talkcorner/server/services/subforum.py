from typing import List

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException
from talkcorner.server.api.api_v1.exceptions.forum import ForumNotCreatorError
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.subforum import Subforum, SubforumCreate, SubforumUpdate
from talkcorner.server.schemas.user import User


async def get_subforums(
    *,
    offset: int,
    limit: int,
    holder: DatabaseHolder
) -> List[Subforum]:
    return await holder.subforum.read_all(offset=offset, limit=limit)


async def get_subforum(
    *,
    subforum_id: int,
    holder: DatabaseHolder
) -> Subforum:
    return await holder.subforum.read_by_id(subforum_id=subforum_id)


async def create_subforum(
    *,
    subforum_create: SubforumCreate,
    holder: DatabaseHolder,
    user: User
) -> Subforum:
    parent_forum = await holder.forum.read_by_id(forum_id=subforum_create.parent_forum_id)

    if parent_forum.creator_id != user.id:
        raise ForumNotCreatorError(forum_id=parent_forum.id)

    child_forum = await holder.forum.read_by_id(forum_id=subforum_create.child_forum_id)

    if child_forum.creator_id != user.id:
        raise ForumNotCreatorError(forum_id=child_forum.id)

    try:
        created_subforum = await holder.subforum.create(
            parent_forum_id=subforum_create.parent_forum_id,
            child_forum_id=subforum_create.child_forum_id,
            creator_id=user.id
        )
        await holder.commit()
    except BaseAppException as e:
        await holder.rollback()
        raise e

    return created_subforum


async def update_subforum(
    *,
    subforum_id: int,
    subforum_update: SubforumUpdate,
    holder: DatabaseHolder,
    user: User
) -> Subforum:
    if subforum_update.parent_forum_id:
        parent_forum = await holder.forum.read_by_id(forum_id=subforum_update.parent_forum_id)

        if parent_forum.creator_id != user.id:
            raise ForumNotCreatorError(forum_id=parent_forum.id)

    if subforum_update.child_forum_id:
        child_forum = await holder.forum.read_by_id(forum_id=subforum_update.child_forum_id)

        if child_forum.creator_id != user.id:
            raise ForumNotCreatorError(forum_id=child_forum.id)

    try:
        updated_subforum = await holder.subforum.update(
            subforum_id=subforum_id,
            creator_id=user.id,
            subforum_update=subforum_update
        )
        await holder.commit()
    except BaseAppException as e:
        await holder.rollback()
        raise e

    return updated_subforum


async def delete_subforum(
    *,
    subforum_id: int,
    holder: DatabaseHolder,
    user: User
) -> Subforum:
    deleted_subforum = await holder.subforum.delete(subforum_id=subforum_id, creator_id=user.id)
    await holder.commit()

    return deleted_subforum
