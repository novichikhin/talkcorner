import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto, exceptions
from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class TopicRepository(Repository[models.Topic]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Topic, session=session)

    async def read_all(self, offset: int, limit: int) -> list[dto.Topic]:
        topics = await self._read_all(offset=offset, limit=limit)

        return [topic.to_dto() for topic in topics]

    async def read_by_id(self, topic_id: uuid.UUID) -> Optional[dto.Topic]:
        topic = await self._read_by_id(id=topic_id)

        return topic.to_dto() if topic else None

    async def update(
            self,
            topic_id: uuid.UUID,
            creator_id: uuid.UUID,
            data: dict
    ) -> Optional[dto.Topic]:
        try:
            topic: Optional[models.Topic] = await self._update(
                models.Topic.id == topic_id,
                models.Topic.creator_id == creator_id,
                **data
            )
        except IntegrityError:
            await self._session.rollback()
            raise exceptions.UnableUpdateTopic
        else:
            return topic.to_dto() if topic else None

    async def create(
            self,
            forum_id: int,
            title: str,
            body: str,
            creator_id: uuid.UUID
    ) -> dto.Topic:
        stmt = sa.insert(models.Topic).values(
            forum_id=forum_id,
            title=title,
            body=body,
            creator_id=creator_id
        ).returning(models.Topic)

        result: sa.ScalarResult[models.Topic] = await self._session.scalars(
            sa.select(models.Topic).from_statement(stmt)
        )
        await self._session.commit()

        return (topic := result.one()).to_dto()

    async def delete(
            self,
            topic_id: uuid.UUID,
            creator_id: uuid.UUID
    ) -> Optional[dto.Topic]:
        topic: Optional[models.Topic] = await self._delete(
            models.Topic.id == topic_id,
            models.Topic.creator_id == creator_id
        )

        return topic.to_dto() if topic else None
