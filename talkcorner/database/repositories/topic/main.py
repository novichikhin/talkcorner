import uuid
from typing import Optional, List

from sqlalchemy import update, ScalarResult, select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, DBAPIError

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.exceptions.forum import ForumNotFoundError
from talkcorner.exceptions.topic.main import (
    TopicNotFoundError,
    TopicNotPatchedError,
    TopicNotDeletedError,
)
from talkcorner.database import models
from talkcorner.database.repositories.base import BaseRepository
from talkcorner.schemas.topic.main import Topic, TopicPatch


class TopicRepository(BaseRepository[models.Topic]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Topic, session=session)

    async def read_all(self, offset: int, limit: int) -> List[Topic]:
        topics = await self._read_all(offset=offset, limit=limit)

        return [topic.to_scheme() for topic in topics]

    async def read_by_id(self, topic_id: uuid.UUID) -> Topic:
        topic = await self._read_by_id(id=topic_id)

        if not topic:
            raise TopicNotFoundError(topic_id=topic_id)

        return topic.to_scheme()

    async def patch(  # type: ignore
        self, topic_id: uuid.UUID, creator_id: uuid.UUID, topic_patch: TopicPatch
    ) -> Topic:
        excluded_topic_patch = topic_patch.model_dump(exclude_unset=True)

        stmt = (
            update(models.Topic)
            .where(models.Topic.id == topic_id, models.Topic.creator_id == creator_id)
            .values(**excluded_topic_patch)
            .returning(models.Topic)
        )

        try:
            result: ScalarResult[models.Topic] = await self._session.scalars(
                select(models.Topic).from_statement(stmt)
            )
        except IntegrityError as e:
            self._parse_error(err=e, forum_id=topic_patch.forum_id)
        else:
            topic: Optional[models.Topic] = result.one_or_none()

            if not topic:
                raise TopicNotPatchedError

            return topic.to_scheme()

    async def create(  # type: ignore
        self, forum_id: int, title: str, body: str, creator_id: uuid.UUID
    ) -> Topic:
        stmt = (
            insert(models.Topic)
            .values(forum_id=forum_id, title=title, body=body, creator_id=creator_id)
            .returning(models.Topic)
        )

        try:
            result: ScalarResult[models.Topic] = await self._session.scalars(
                select(models.Topic).from_statement(stmt)
            )
        except IntegrityError as e:
            self._parse_error(err=e, forum_id=forum_id)
        else:
            topic: models.Topic = result.one()

            return topic.to_scheme()

    async def delete(self, topic_id: uuid.UUID, creator_id: uuid.UUID) -> Topic:
        stmt = (
            delete(models.Topic)
            .where(models.Topic.id == topic_id, models.Topic.creator_id == creator_id)
            .returning(models.Topic)
        )

        result: ScalarResult[models.Topic] = await self._session.scalars(
            select(models.Topic).from_statement(stmt)
        )

        topic: Optional[models.Topic] = result.one_or_none()

        if not topic:
            raise TopicNotDeletedError

        return topic.to_scheme()

    def _parse_error(self, *, err: DBAPIError, forum_id: Optional[int]) -> None:
        constraint_name = err.__cause__.__cause__.constraint_name  # type: ignore

        if forum_id and constraint_name == "topics_forum_id_fkey":
            raise ForumNotFoundError(forum_id=forum_id) from err
