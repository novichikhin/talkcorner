import uuid

from typing import Optional, List

from sqlalchemy import update, ScalarResult, select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.exceptions.forum import (
    ForumNotFoundError,
    ForumNotPatchedError,
    ForumNotDeletedError,
)
from talkcorner.database import models
from talkcorner.database.repositories.base import BaseRepository
from talkcorner.schemas.forum import Forum, ForumPatch


class ForumRepository(BaseRepository[models.Forum]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Forum, session=session)

    async def read_all(self, offset: int, limit: int) -> List[Forum]:
        forums = await self._read_all(offset=offset, limit=limit)

        return [forum.to_scheme() for forum in forums]

    async def read_by_id(self, forum_id: int) -> Forum:
        forum = await self._read_by_id(id=forum_id)

        if not forum:
            raise ForumNotFoundError(forum_id=forum_id)

        return forum.to_scheme()

    async def patch(
        self, forum_id: int, creator_id: uuid.UUID, forum_patch: ForumPatch
    ) -> Forum:
        excluded_forum_patch = forum_patch.model_dump(exclude_unset=True)

        stmt = (
            update(models.Forum)
            .where(models.Forum.id == forum_id, models.Forum.creator_id == creator_id)
            .values(**excluded_forum_patch)
            .returning(models.Forum)
        )

        result: ScalarResult[models.Forum] = await self._session.scalars(
            select(models.Forum).from_statement(stmt)
        )

        forum: Optional[models.Forum] = result.one_or_none()

        if not forum:
            raise ForumNotPatchedError

        return forum.to_scheme()

    async def create(
        self, title: str, description: Optional[str], creator_id: uuid.UUID
    ) -> Forum:
        stmt = (
            insert(models.Forum)
            .values(title=title, description=description, creator_id=creator_id)
            .returning(models.Forum)
        )

        result: ScalarResult[models.Forum] = await self._session.scalars(
            select(models.Forum).from_statement(stmt)
        )

        forum: models.Forum = result.one()

        return forum.to_scheme()

    async def delete(self, forum_id: int, creator_id: uuid.UUID) -> Forum:
        stmt = (
            delete(models.Forum)
            .where(models.Forum.id == forum_id, models.Forum.creator_id == creator_id)
            .returning(models.Forum)
        )

        result: ScalarResult[models.Forum] = await self._session.scalars(
            select(models.Forum).from_statement(stmt)
        )

        forum: Optional[models.Forum] = result.one_or_none()

        if not forum:
            raise ForumNotDeletedError

        return forum.to_scheme()
