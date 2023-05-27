import sqlalchemy as sa

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common import dto
from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class UserRepository(Repository[models.User]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.User, session=session)

    async def read_by_id(self, user_id: int) -> Optional[dto.User]:
        user = await self._read_by_id(id=user_id)

        return user.to_dto() if user else None

    async def read_all(self) -> list[dto.User]:
        users = await self._read_all()

        return [user.to_dto() for user in users]

    async def read_by_login(self, username: str) -> Optional[dto.User]:
        result: sa.Result[tuple[models.User]] = await self._session.execute(
            sa.select(models.User).where(models.User.username == username)
        )

        user: Optional[models.User] = result.scalar()

        return user.to_dto() if user else None
