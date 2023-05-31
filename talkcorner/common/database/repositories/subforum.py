from typing import Optional

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

    async def read_by_id(self, forum_id: int) -> Optional[dto.Subforum]:
        subforum = await self._read_by_id(id=forum_id)

        return subforum.to_dto() if subforum else None
