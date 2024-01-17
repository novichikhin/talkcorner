from typing import List

from talkcorner.exceptions.base import BaseAppException
from talkcorner.exceptions.forum import ForumNotCreatorError
from talkcorner.database.holder import DatabaseHolder
from talkcorner.schemas.subforum import Subforum, SubforumCreate, SubforumPatch
from talkcorner.schemas.user import User


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


async def patch_subforum(
    *,
    subforum_id: int,
    subforum_patch: SubforumPatch,
    holder: DatabaseHolder,
    user: User
) -> Subforum:
    if subforum_patch.parent_forum_id:
        parent_forum = await holder.forum.read_by_id(forum_id=subforum_patch.parent_forum_id)

        if parent_forum.creator_id != user.id:
            raise ForumNotCreatorError(forum_id=parent_forum.id)

    if subforum_patch.child_forum_id:
        child_forum = await holder.forum.read_by_id(forum_id=subforum_patch.child_forum_id)

        if child_forum.creator_id != user.id:
            raise ForumNotCreatorError(forum_id=child_forum.id)

    try:
        patched_subforum = await holder.subforum.patch(
            subforum_id=subforum_id,
            creator_id=user.id,
            subforum_patch=subforum_patch
        )
        await holder.commit()
    except BaseAppException as e:
        await holder.rollback()
        raise e

    return patched_subforum


async def delete_subforum(
    *,
    subforum_id: int,
    holder: DatabaseHolder,
    user: User
) -> Subforum:
    deleted_subforum = await holder.subforum.delete(subforum_id=subforum_id, creator_id=user.id)
    await holder.commit()

    return deleted_subforum
