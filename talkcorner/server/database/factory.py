from typing import AsyncGenerator, Callable, Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from talkcorner.server.database.holder import DatabaseHolder


def sa_build_connection_uri(
        *,
        driver: str,
        host: str,
        port: int,
        user: str,
        password: str,
        db: str
) -> str:
    url = URL.create(
        drivername=driver,
        username=user,
        password=password,
        host=host,
        port=port,
        database=db
    )

    return f"postgresql+{url.render_as_string(hide_password=False)}"


def sa_create_engine(connection_uri: str, **engine_kwargs) -> AsyncEngine:
    return create_async_engine(url=connection_uri, **engine_kwargs)


def sa_create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


def sa_create_holder(session_factory: async_sessionmaker[AsyncSession]) -> Callable[[], AsyncGenerator[Any, Any]]:
    async def wrapper():
        async with session_factory() as session:
            yield DatabaseHolder(session=session)

    return wrapper
