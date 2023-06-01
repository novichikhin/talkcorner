from typing import AsyncGenerator, Any

import pytest
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from talkcorner.common.database.holder import DatabaseHolder


@pytest.fixture(scope="function")
async def holder(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[Any, Any]:
    async with session_factory() as session:
        yield DatabaseHolder(session=session)


@pytest.fixture(scope="session")
def crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")
