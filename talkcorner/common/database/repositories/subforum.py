import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto
from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class SubforumRepository(Repository[models.Subforum]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Subforum, session=session)

    async def read_all(self, offset: int, limit: int) -> list[dto.Subforum]:
        subforums = await self._read_all(offset=offset, limit=limit)

        return [subforum.to_dto() for subforum in subforums]

    async def read_by_id(self, subforum_id: int) -> Optional[dto.Subforum]:
        subforum = await self._read_by_id(id=subforum_id)

        return subforum.to_dto() if subforum else None

    async def update(
            self,
            subforum_id: int,
            creator_id: uuid.UUID,
            data: dict
    ) -> Optional[dto.Subforum]:
        stmt = sa.update(models.Subforum).where(
            models.Subforum.id == subforum_id,
            models.Subforum.creator_id == creator_id
        ).values(
            **data
        ).returning(models.Subforum)

        result = await self._session.execute(
            sa.select(models.Subforum).from_statement(stmt)
        )

        await self._session.commit()

        subforum: Optional[models.Subforum] = result.scalar()

        return subforum.to_dto() if subforum else None

    async def create(
            self,
            parent_forum_id: int,
            child_forum_id: int,
            creator_id: uuid.UUID
    ) -> Optional[dto.Subforum]:
        stmt = insert(models.Subforum).values(
            parent_forum_id=parent_forum_id,
            child_forum_id=child_forum_id,
            creator_id=creator_id
        ).on_conflict_do_nothing(
            index_elements=[models.Subforum.parent_forum_id, models.Subforum.child_forum_id]
        ).returning(models.Subforum)

        result = await self._session.execute(
            sa.select(models.Subforum).from_statement(stmt)
        )
        await self._session.commit()

        subforum: Optional[models.Subforum] = result.scalar()

        return subforum.to_dto() if subforum else None

    async def delete(
            self,
            subforum_id: int,
            creator_id: uuid.UUID
    ) -> Optional[dto.Subforum]:
        stmt = sa.delete(models.Subforum).where(
            models.Subforum.id == subforum_id,
            models.Subforum.creator_id == creator_id
        ).returning(models.Subforum)

        result: sa.ScalarResult[models.Subforum] = await self._session.scalars(
            sa.select(models.Subforum).from_statement(stmt)
        )
        await self._session.commit()

        subforum: Optional[models.Subforum] = result.first()

        return subforum.to_dto() if subforum else None
