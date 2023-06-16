import uuid
from typing import Optional, NoReturn

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, DBAPIError

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto, exceptions
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
        try:
            subforum: Optional[models.Subforum] = await self._update(
                models.Subforum.id == subforum_id,
                models.Subforum.creator_id == creator_id,
                **data
            )
        except IntegrityError:
            await self._session.rollback()
            raise exceptions.UnableUpdateSubforum
        else:
            return subforum.to_dto() if subforum else None

    async def create(
            self,
            parent_forum_id: int,
            child_forum_id: int,
            creator_id: uuid.UUID
    ) -> dto.Subforum:
        stmt = insert(models.Subforum).values(
            parent_forum_id=parent_forum_id,
            child_forum_id=child_forum_id,
            creator_id=creator_id
        ).returning(models.Subforum)

        try:
            result: sa.ScalarResult[models.Subforum] = await self._session.scalars(
                sa.select(models.Subforum).from_statement(stmt)
            )
            await self._session.commit()
        except IntegrityError as err:
            await self._session.rollback()
            self._parse_create_error(err)
        else:
            return (subforum := result.one()).to_dto()

    async def delete(
            self,
            subforum_id: int,
            creator_id: uuid.UUID
    ) -> Optional[dto.Subforum]:
        subforum: Optional[models.Subforum] = await self._delete(
            models.Subforum.id == subforum_id,
            models.Subforum.creator_id == creator_id
        )

        return subforum.to_dto() if subforum else None

    def _parse_create_error(self, err: DBAPIError) -> NoReturn:
        constraint_name = err.__cause__.__cause__.constraint_name # type: ignore

        if constraint_name == "subforums_parent_child_forums":
            raise exceptions.ParentChildForumsAlreadyExists from err
        else:
            raise exceptions.UnableCreateSubforum from err
