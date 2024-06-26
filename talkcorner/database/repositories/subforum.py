import uuid
from typing import Optional, List

from sqlalchemy import update, ScalarResult, select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, DBAPIError

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.exceptions.subforum import (
    SubforumNotFoundError,
    SubforumNotPatchedError,
    ParentChildForumsAlreadyExistsError,
    SubforumNotDeletedError,
)
from talkcorner.database import models
from talkcorner.database.repositories.base import BaseRepository
from talkcorner.schemas.subforum import Subforum, SubforumPatch


class SubforumRepository(BaseRepository[models.Subforum]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Subforum, session=session)

    async def read_all(self, offset: int, limit: int) -> List[Subforum]:
        subforums = await self._read_all(offset=offset, limit=limit)

        return [subforum.to_scheme() for subforum in subforums]

    async def read_by_id(self, subforum_id: int) -> Subforum:
        subforum = await self._read_by_id(id=subforum_id)

        if not subforum:
            raise SubforumNotFoundError(subforum_id=subforum_id)

        return subforum.to_scheme()

    async def patch(  # type: ignore
        self, subforum_id: int, creator_id: uuid.UUID, subforum_patch: SubforumPatch
    ) -> Subforum:
        excluded_subforum_patch = subforum_patch.model_dump(exclude_unset=True)

        stmt = (
            update(models.Subforum)
            .where(
                models.Subforum.id == subforum_id,
                models.Subforum.creator_id == creator_id,
            )
            .values(**excluded_subforum_patch)
            .returning(models.Subforum)
        )

        try:
            result: ScalarResult[models.Subforum] = await self._session.scalars(
                select(models.Subforum).from_statement(stmt)
            )
        except IntegrityError as e:
            self._parse_error(err=e)
        else:
            subforum: Optional[models.Subforum] = result.one_or_none()

            if not subforum:
                raise SubforumNotPatchedError

            return subforum.to_scheme()

    async def create(  # type: ignore
        self, parent_forum_id: int, child_forum_id: int, creator_id: uuid.UUID
    ) -> Subforum:
        stmt = (
            insert(models.Subforum)
            .values(
                parent_forum_id=parent_forum_id,
                child_forum_id=child_forum_id,
                creator_id=creator_id,
            )
            .returning(models.Subforum)
        )

        try:
            result: ScalarResult[models.Subforum] = await self._session.scalars(
                select(models.Subforum).from_statement(stmt)
            )
        except IntegrityError as e:
            self._parse_error(err=e)
        else:
            subforum: models.Subforum = result.one()

            return subforum.to_scheme()

    async def delete(self, subforum_id: int, creator_id: uuid.UUID) -> Subforum:
        stmt = (
            delete(models.Subforum)
            .where(
                models.Subforum.id == subforum_id,
                models.Subforum.creator_id == creator_id,
            )
            .returning(models.Subforum)
        )

        result: ScalarResult[models.Subforum] = await self._session.scalars(
            select(models.Subforum).from_statement(stmt)
        )

        subforum: Optional[models.Subforum] = result.one_or_none()

        if not subforum:
            raise SubforumNotDeletedError

        return subforum.to_scheme()

    def _parse_error(self, err: DBAPIError) -> None:
        constraint_name = err.__cause__.__cause__.constraint_name  # type: ignore

        if constraint_name == "subforums_parent_child_forums":
            raise ParentChildForumsAlreadyExistsError from err
