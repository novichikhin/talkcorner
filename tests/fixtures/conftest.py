from typing import AsyncGenerator, Any

import nats
import pytest
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from talkcorner.database.holder import DatabaseHolder
from tests.mocks.nats import JetStreamContextMock


@pytest.fixture(scope="function")
async def holder(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[Any, Any]:
    async with session_factory() as session:
        yield DatabaseHolder(session=session)


@pytest.fixture(scope="session")
def crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
def nats_mock() -> JetStreamContextMock:
    return JetStreamContextMock(conn=nats.NATS())
