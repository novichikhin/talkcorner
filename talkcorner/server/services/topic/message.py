import uuid
from typing import List

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.topic.message import TopicMessage, TopicMessageCreate, TopicMessagePatch
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


async def patch_topic_message(
    *,
    topic_message_id: uuid.UUID,
    topic_message_patch: TopicMessagePatch,
    holder: DatabaseHolder,
    user: User
) -> TopicMessage:
    patched_topic_message = await holder.topic_message.patch(
        topic_message_id=topic_message_id,
        creator_id=user.id,
        topic_message_patch=topic_message_patch
    )
    await holder.commit()

    return patched_topic_message


async def delete_topic_message(
    *,
    topic_message_id: uuid.UUID,
    holder: DatabaseHolder,
    user: User
) -> TopicMessage:
    deleted_topic_message = await holder.topic_message.delete(
        topic_message_id=topic_message_id,
        creator_id=user.id
    )
    await holder.commit()

    return deleted_topic_message
