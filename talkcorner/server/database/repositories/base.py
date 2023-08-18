import sqlalchemy as sa

from abc import ABC
from typing import (
    TypeVar,
    Generic,
    Optional,
    Sequence,
    Type,
    Any
)

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.server.database.models.base import BaseModel

Model = TypeVar("Model", bound=BaseModel)


class BaseRepository(ABC, Generic[Model]):

    def __init__(self, model: Type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def _read_by_id(self, id: Any) -> Optional[Model]:
        return await self._session.get(self._model, id)

    async def _read_all(self, offset: int, limit: int) -> Sequence[Model]:
        result: sa.ScalarResult[Model] = await self._session.scalars(
            sa.select(self._model).offset(offset).limit(limit)
        )

        return result.all()
