import uuid

import sqlalchemy as sa

from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto, exceptions
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

    async def update(
            self,
            forum_id: int,
            creator_id: uuid.UUID,
            data: dict
    ) -> Optional[dto.Forum]:
        try:
            forum: Optional[models.Forum] = await self._update(
                models.Forum.id == forum_id,
                models.Forum.creator_id == creator_id,
                **data
            )
        except IntegrityError as e:
            await self._session.rollback()
            raise exceptions.UnableInteraction from e
        else:
            return forum.to_dto() if forum else None

    async def create(
            self,
            title: str,
            description: Optional[str],
            creator_id: uuid.UUID
    ) -> dto.Forum:
        stmt = sa.insert(models.Forum).values(
            title=title,
            description=description,
            creator_id=creator_id
        ).returning(models.Forum)

        result: sa.ScalarResult[models.Forum] = await self._session.scalars(
            sa.select(models.Forum).from_statement(stmt)
        )
        await self._session.commit()

        return (forum := result.one()).to_dto()

    async def delete(
            self,
            forum_id: int,
            creator_id: uuid.UUID
    ) -> Optional[dto.Forum]:
        forum: Optional[models.Forum] = await self._delete(
            models.Forum.id == forum_id,
            models.Forum.creator_id == creator_id
        )

        return forum.to_dto() if forum else None
