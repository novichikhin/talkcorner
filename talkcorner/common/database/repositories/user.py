from typing import Optional

import sqlalchemy as sa

from talkcorner.common import dto
from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class UserRepository(Repository):

    async def read_by_id(self, user_id: int) -> Optional[dto.User]:
        result: sa.Result[tuple[models.User]] = await self._session.execute(
            sa.select(models.User).where(
                models.User.id == user_id
            )
        )

        user: Optional[models.User] = result.scalar()

        return user.to_dto() if user else None

    async def read_all(self) -> list[dto.User]:
        results: sa.ScalarResult[models.User] = await self._session.scalars(sa.select(models.User))

        return [user.to_dto() for user in results.all()]
