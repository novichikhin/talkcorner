import uuid
from typing import Optional, List

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, DBAPIError

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.exceptions.topic.main import TopicNotFoundError
from talkcorner.exceptions.topic.message import (
    TopicMessageNotFoundError,
    TopicMessageNotPatchedError,
    TopicMessageNotDeletedError,
)
from talkcorner.database import models
from talkcorner.database.repositories.base import BaseRepository
from talkcorner.schemas.topic.message import TopicMessage, TopicMessagePatch


class TopicMessageRepository(BaseRepository[models.TopicMessage]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.TopicMessage, session=session)

    async def read_all(self, offset: int, limit: int) -> List[TopicMessage]:
        topic_messages = await self._read_all(offset=offset, limit=limit)

        return [topic_message.to_scheme() for topic_message in topic_messages]

    async def read_by_id(self, topic_message_id: uuid.UUID) -> TopicMessage:
        topic_message = await self._read_by_id(id=topic_message_id)

        if not topic_message:
            raise TopicMessageNotFoundError(topic_message_id=topic_message_id)

        return topic_message.to_scheme()

    async def patch(
        self,
        topic_message_id: uuid.UUID,
        creator_id: uuid.UUID,
        topic_message_patch: TopicMessagePatch,
    ) -> TopicMessage:
        excluded_topic_message_patch = topic_message_patch.model_dump(
            exclude_unset=True
        )

        stmt = (
            sa.update(models.TopicMessage)
            .where(
                models.TopicMessage.id == topic_message_id,
                models.TopicMessage.creator_id == creator_id,
            )
            .values(**excluded_topic_message_patch)
            .returning(models.TopicMessage)
        )

        result: sa.ScalarResult[models.TopicMessage] = await self._session.scalars(
            sa.select(models.TopicMessage).from_statement(stmt)
        )

        topic_message: Optional[models.TopicMessage] = result.one_or_none()

        if not topic_message:
            raise TopicMessageNotPatchedError

        return topic_message.to_scheme()

    async def create(  # type: ignore
        self, topic_id: uuid.UUID, body: str, creator_id: uuid.UUID
    ) -> TopicMessage:
        stmt = (
            sa.insert(models.TopicMessage)
            .values(topic_id=topic_id, body=body, creator_id=creator_id)
            .returning(models.TopicMessage)
        )

        try:
            result: sa.ScalarResult[models.TopicMessage] = await self._session.scalars(
                sa.select(models.TopicMessage).from_statement(stmt)
            )
        except IntegrityError as e:
            self._parse_error(err=e, topic_id=topic_id)
        else:
            topic_message: models.TopicMessage = result.one()

            return topic_message.to_scheme()

    async def delete(
        self, topic_message_id: uuid.UUID, creator_id: uuid.UUID
    ) -> TopicMessage:
        stmt = (
            sa.delete(models.TopicMessage)
            .where(
                models.TopicMessage.id == topic_message_id,
                models.TopicMessage.creator_id == creator_id,
            )
            .returning(models.TopicMessage)
        )

        result: sa.ScalarResult[models.TopicMessage] = await self._session.scalars(
            sa.select(models.TopicMessage).from_statement(stmt)
        )

        topic_message: Optional[models.TopicMessage] = result.one_or_none()

        if not topic_message:
            raise TopicMessageNotDeletedError

        return topic_message.to_scheme()

    def _parse_error(self, *, err: DBAPIError, topic_id: uuid.UUID) -> None:
        constraint_name = err.__cause__.__cause__.constraint_name  # type: ignore

        if constraint_name == "topic_messages_topic_id_fkey":
            raise TopicNotFoundError(topic_id=topic_id) from err
