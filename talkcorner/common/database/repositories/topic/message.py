import uuid
from typing import Optional, NoReturn

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, DBAPIError

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

    async def read_by_id(self, topic_message_id: uuid.UUID) -> Optional[dto.TopicMessage]:
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
        except IntegrityError as e:
            await self._session.rollback()
            self._parse_error(err=e)
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

        try:
            result: sa.ScalarResult[models.TopicMessage] = await self._session.scalars(
                sa.select(models.TopicMessage).from_statement(stmt)
            )
            await self._session.commit()
        except IntegrityError as e:
            await self._session.rollback()
            self._parse_error(err=e)
        else:
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

    def _parse_error(self, err: DBAPIError) -> NoReturn:
        constraint_name = err.__cause__.__cause__.constraint_name # type: ignore

        if constraint_name == "topic_messages_topic_id_fkey":
            raise exceptions.TopicNotFound from err

        raise exceptions.UnableInteraction from err
