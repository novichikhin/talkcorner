import uuid

import sqlalchemy as sa

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto
from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class ForumRepository(Repository[models.Forum]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Forum, session=session)

    async def read_all(self, offset: int, limit: int) -> list[dto.Forum]:
        forums = await self._read_all(offset=offset, limit=limit)

        return [forum.to_dto() for forum in forums]

    async def read_by_id(self, forum_id: int) -> Optional[dto.Forum]:
        forum = await self._read_by_id(id=forum_id)

        return forum.to_dto() if forum else None

    async def create(
            self,
            title: str,
            description: Optional[str],
            creator_id: uuid.UUID
    ) -> Optional[dto.Forum]:
        stmt = sa.insert(models.Forum).values(
            title=title,
            description=description,
            creator_id=creator_id
        ).returning(models.Forum)

        result: sa.ScalarResult[models.Forum] = await self._session.scalars(
            sa.select(models.Forum).from_statement(stmt)
        )
        await self._session.commit()

        forum: Optional[models.Forum] = result.first()

        return forum.to_dto() if forum else None

    async def delete(
            self,
            forum_id: int,
            creator_id: uuid.UUID
    ) -> Optional[dto.Forum]:
        stmt = sa.delete(models.Forum).where(
            models.Forum.id == forum_id,
            models.Forum.creator_id == creator_id
        ).returning(models.Forum)

        result: sa.ScalarResult[models.Forum] = await self._session.scalars(
            sa.select(models.Forum).from_statement(stmt)
        )
        await self._session.commit()

        forum: Optional[models.Forum] = result.first()

        return forum.to_dto() if forum else None
