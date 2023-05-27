import uuid

import sqlalchemy as sa

from abc import ABC
from typing import TypeVar, Generic, Optional, Union, Sequence, Type

from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common.database.models.main import Base

Model = TypeVar("Model", bound=Base)
Id = Union[int, uuid.UUID]


class Repository(ABC, Generic[Model]):

    def __init__(self, model: Type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def _read_by_id(self, id: Id) -> Optional[Model]:
        return await self._session.get(self._model, id)

    async def _read_all(self, offset: int, limit: int) -> Sequence[Model]:
        result: sa.ScalarResult[Model] = await self._session.scalars(
            sa.select(self._model).offset(offset).limit(limit)
        )

        return result.all()
