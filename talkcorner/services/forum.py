from typing import List

from talkcorner.database.holder import DatabaseHolder
from talkcorner.schemas.forum import Forum, ForumCreate, ForumPatch
from talkcorner.schemas.user import User


async def get_forums(
    *,
    offset: int,
    limit: int,
    holder: DatabaseHolder
) -> List[Forum]:
    return await holder.forum.read_all(offset=offset, limit=limit)


async def get_forum(
    *,
    forum_id: int,
    holder: DatabaseHolder
) -> Forum:
    return await holder.forum.read_by_id(forum_id=forum_id)


async def create_forum(
    *,
    forum_create: ForumCreate,
    holder: DatabaseHolder,
    user: User
) -> Forum:
    created_forum = await holder.forum.create(
        title=forum_create.title,
        description=forum_create.description,
        creator_id=user.id
    )
    await holder.commit()

    return created_forum


async def patch_forum(
    *,
    forum_id: int,
    forum_patch: ForumPatch,
    holder: DatabaseHolder,
    user: User
) -> Forum:
    updated_forum = await holder.forum.patch(
        forum_id=forum_id,
        creator_id=user.id,
        forum_patch=forum_patch
    )
    await holder.commit()

    return updated_forum


async def delete_forum(
    *,
    forum_id: int,
    holder: DatabaseHolder,
    user: User
) -> Forum:
    deleted_forum = await holder.forum.delete(forum_id=forum_id, creator_id=user.id)
    await holder.commit()

    return deleted_forum
