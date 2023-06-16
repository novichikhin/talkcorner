import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto, exceptions
from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class TopicMessageRepository(Repository[models.TopicMessage]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.TopicMessage, session=session)

    async def read_all(self, offset: int, limit: int) -> list[dto.TopicMessage]:
        topic_messages = await self._read_all(offset=offset, limit=limit)

        return [topic_message.to_dto() for topic_message in topic_messages]

    async def read_by_id(self, topic_message_id: int) -> Optional[dto.TopicMessage]:
        topic_message = await self._read_by_id(id=topic_message_id)

        return topic_message.to_dto() if topic_message else None

    async def update(
            self,
            topic_message_id: uuid.UUID,
            creator_id: uuid.UUID,
            data: dict
    ) -> Optional[dto.TopicMessage]:
        try:
            topic_message: Optional[models.TopicMessage] = await self._update(
                models.TopicMessage.id == topic_message_id,
                models.TopicMessage.creator_id == creator_id,
                **data
            )
        except IntegrityError:
            await self._session.rollback()
            raise exceptions.UnableUpdateTopicMessage
        else:
            return topic_message.to_dto() if topic_message else None

    async def create(
            self,
            topic_id: uuid.UUID,
            body: str,
            creator_id: uuid.UUID
    ) -> dto.TopicMessage:
        stmt = sa.insert(models.TopicMessage).values(
            topic_id=topic_id,
            body=body,
            creator_id=creator_id
        ).returning(models.TopicMessage)

        result: sa.ScalarResult[models.TopicMessage] = await self._session.scalars(
            sa.select(models.TopicMessage).from_statement(stmt)
        )
        await self._session.commit()

        return (topic_message := result.one()).to_dto()

    async def delete(
            self,
            topic_message_id: uuid.UUID,
            creator_id: uuid.UUID
    ) -> Optional[dto.TopicMessage]:
        topic_message: Optional[models.TopicMessage] = await self._delete(
            models.TopicMessage.id == topic_message_id,
            models.TopicMessage.creator_id == creator_id
        )

        return topic_message.to_dto() if topic_message else None
