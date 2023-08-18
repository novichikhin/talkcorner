from typing import List

from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.forum import Forum, ForumCreate, ForumUpdate
from talkcorner.server.schemas.user import User


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


async def update_forum(
    *,
    forum_id: int,
    forum_update: ForumUpdate,
    holder: DatabaseHolder,
    user: User
) -> Forum:
    updated_forum = await holder.forum.update(
        forum_id=forum_id,
        creator_id=user.id,
        forum_update=forum_update
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
