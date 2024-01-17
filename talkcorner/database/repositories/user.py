import uuid

import sqlalchemy as sa

from typing import Optional, List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.exceptions.user import (
    UserNotFoundError,
    AuthenticationUserNotFoundError,
    WrongUsernameOrPasswordError,
    EmailNotVerifiedError,
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError
)
from talkcorner.database import models
from talkcorner.database.repositories.base import BaseRepository
from talkcorner.schemas.user import User


class UserRepository(BaseRepository[models.User]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.User, session=session)

    async def read_by_authenticate(self, user_id: uuid.UUID) -> User:
        user = await self._read_by_id(id=user_id)

        if not user:
            raise AuthenticationUserNotFoundError(user_id=user_id)

        return user.to_scheme()

    async def read_by_id(self, user_id: uuid.UUID) -> User:
        user = await self._read_by_id(id=user_id)

        if not user:
            raise UserNotFoundError(user_id=user_id)

        return user.to_scheme()

    async def read_all(self, offset: int, limit: int) -> List[User]:
        users = await self._read_all(offset=offset, limit=limit)

        return [user.to_scheme() for user in users]

    async def read_by_login(self, username: str) -> User:
        result: sa.ScalarResult[models.User] = await self._session.scalars(
            sa.select(models.User).where(models.User.username == username)
        )

        user: Optional[models.User] = result.first()

        if not user:
            raise WrongUsernameOrPasswordError

        return user.to_scheme()

    async def verify_email(self, user_id: uuid.UUID) -> User:
        stmt = sa.update(models.User).where(
            models.User.id == user_id
        ).values(email_verified=True).returning(models.User)

        result = await self._session.scalars(
            sa.select(models.User).from_statement(stmt)
        )

        user: Optional[models.User] = result.first()

        if not user:
            raise EmailNotVerifiedError

        return user.to_scheme()

    async def create( # type: ignore
        self,
        username: str,
        password: str,
        email: str,
        email_verified: bool = False
    ) -> User:
        stmt = insert(models.User).values(
            username=username,
            password=password,
            email=email,
            email_verified=email_verified
        ).returning(models.User)

        try:
            result: sa.ScalarResult[models.User] = await self._session.scalars(
                sa.select(models.User).from_statement(stmt)
            )
        except IntegrityError as e:
            self._parse_error_on_create(err=e)
        else:
            user: models.User = result.one()

            return user.to_scheme()

    def _parse_error_on_create(self, err: DBAPIError) -> None:
        constraint_name = err.__cause__.__cause__.constraint_name # type: ignore

        if constraint_name == "users_email_key":
            raise EmailAlreadyExistsError from err
        elif constraint_name == "users_username_key":
            raise UsernameAlreadyExistsError from err
