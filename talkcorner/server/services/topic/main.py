import uuid
from typing import List

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.topic.main import Topic, TopicCreate, TopicUpdate
from talkcorner.server.schemas.user import User


async def get_topics(
    *,
    offset: int,
    limit: int,
    holder: DatabaseHolder
) -> List[Topic]:
    return await holder.topic.read_all(offset=offset, limit=limit)


async def get_topic(
    *,
    topic_id: uuid.UUID,
    holder: DatabaseHolder
) -> Topic:
    return await holder.topic.read_by_id(topic_id=topic_id)


async def create_topic(
    *,
    topic_create: TopicCreate,
    holder: DatabaseHolder,
    user: User
) -> Topic:
    try:
        created_topic = await holder.topic.create(
            forum_id=topic_create.forum_id,
            title=topic_create.title,
            body=topic_create.body,
            creator_id=user.id
        )
        await holder.commit()
    except BaseAppException as e:
        await holder.rollback()
        raise e
    else:
        return created_topic


async def update_topic(
    *,
    topic_id: uuid.UUID,
    topic_update: TopicUpdate,
    holder: DatabaseHolder,
    user: User
) -> Topic:
    try:
        updated_topic = await holder.topic.update(
            topic_id=topic_id,
            creator_id=user.id,
            topic_update=topic_update
        )
        await holder.commit()
    except BaseAppException as e:
        await holder.rollback()
        raise e
    else:
        return updated_topic


async def delete_topic(
    *,
    topic_id: uuid.UUID,
    holder: DatabaseHolder,
    user: User
) -> Topic:
    deleted_topic = await holder.topic.delete(topic_id=topic_id, creator_id=user.id)
    await holder.commit()

    return deleted_topic
