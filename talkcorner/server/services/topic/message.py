import uuid
from typing import List

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.topic.message import TopicMessage, TopicMessageCreate, TopicMessageUpdate
from talkcorner.server.schemas.user import User


async def get_topic_messages(
    *,
    offset: int,
    limit: int,
    holder: DatabaseHolder
) -> List[TopicMessage]:
    return await holder.topic_message.read_all(offset=offset, limit=limit)


async def get_topic_message(
    *,
    topic_message_id: uuid.UUID,
    holder: DatabaseHolder
) -> TopicMessage:
    return await holder.topic_message.read_by_id(topic_message_id=topic_message_id)


async def create_topic_message(
    *,
    topic_message_create: TopicMessageCreate,
    holder: DatabaseHolder,
    user: User
) -> TopicMessage:
    try:
        created_topic_message = await holder.topic_message.create(
            topic_id=topic_message_create.topic_id,
            body=topic_message_create.body,
            creator_id=user.id
        )
        await holder.commit()
    except BaseAppException as e:
        await holder.rollback()
        raise e

    return created_topic_message


async def update_topic_message(
    *,
    topic_message_id: uuid.UUID,
    topic_message_update: TopicMessageUpdate,
    holder: DatabaseHolder,
    user: User
) -> TopicMessage:
    updated_topic_message = await holder.topic_message.update(
        topic_message_id=topic_message_id,
        creator_id=user.id,
        topic_message_update=topic_message_update
    )
    await holder.commit()

    return updated_topic_message


async def delete_topic_message(
    *,
    topic_message_id: uuid.UUID,
    holder: DatabaseHolder,
    user: User
) -> TopicMessage:
    deleted_topic_message = await holder.topic_message.delete(topic_message_id=topic_message_id, creator_id=user.id)
    await holder.commit()

    return deleted_topic_message
