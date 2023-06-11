import uuid

import sqlalchemy as sa

from typing import Optional, NoReturn

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto, exceptions
from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class UserRepository(Repository[models.User]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.User, session=session)

    async def read_by_id(self, user_id: uuid.UUID) -> Optional[dto.User]:
        user = await self._read_by_id(id=user_id)

        return user.to_dto() if user else None

    async def read_all(self, offset: int, limit: int) -> list[dto.User]:
        users = await self._read_all(offset=offset, limit=limit)

        return [user.to_dto() for user in users]

    async def read_by_login(self, username: str) -> Optional[dto.User]:
        result: sa.ScalarResult[models.User] = await self._session.scalars(
            sa.select(models.User).where(models.User.username == username)
        )

        user: Optional[models.User] = result.first()

        return user.to_dto() if user else None

    async def create(
            self,
            username: str,
            password: str,
            email: str
    ) -> dto.User:
        stmt = insert(models.User).values(
            username=username,
            password=password,
            email=email
        ).returning(models.User)

        try:
            result: sa.ScalarResult[models.User] = await self._session.scalars(
                sa.select(models.User).from_statement(stmt)
            )
            await self._session.commit()
        except IntegrityError as err:
            await self._session.rollback()
            self._parse_create_error(err)
        else:
            return (user := result.one()).to_dto()

    def _parse_create_error(self, err: DBAPIError) -> NoReturn:
        constraint_name = err.__cause__.__cause__.constraint_name # type: ignore

        if constraint_name == "users_email_key":
            raise exceptions.EmailAlreadyExists from err
        elif constraint_name == "users_username_key":
            raise exceptions.UsernameAlreadyExists from err
        else:
            raise exceptions.UnableCreateUser from err
