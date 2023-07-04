import os

import sqlalchemy as sa
import pytest_asyncio

from typing import Generator

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker, close_all_sessions
from testcontainers.postgres import PostgresContainer

from talkcorner.common import types
from talkcorner.common.database.models.main import Base
from talkcorner.server.api.api_v1.dependencies.database import DatabaseSessionMarker
from talkcorner.server.api.setup import register_app
from tests.fixtures.conftest import holder, crypt_context # noqa: F401
from tests.fixtures.user import create_user # noqa: F401
from tests.fixtures.auth_token import create_auth_access_token, create_auth_refresh_token # noqa: F401


@pytest.fixture(scope="session", autouse=True)
def app(postgres_url: str) -> FastAPI:
    settings = types.Setting(_env_file=".env.example").copy(
        update={"database_uri": postgres_url.replace("psycopg2", "asyncpg")}
    )

    return register_app(settings=settings)


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(session_factory: sessionmaker) -> None:
    async with session_factory() as session:
        for table in Base.metadata.tables:
            await session.execute(sa.text(f"TRUNCATE TABLE {table} CASCADE;"))
        await session.commit()


@pytest.fixture(scope="session")
def session_factory(app: FastAPI) -> Generator[sessionmaker, None, None]:
    _session_factory = app.dependency_overrides[DatabaseSessionMarker]()

    yield _session_factory

    close_all_sessions()


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    """
        thx github.com/bomzheg/Shvatka
    """
    postgres = PostgresContainer("postgres:latest")
    if os.name == "nt":
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        yield postgres.get_connection_url()
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    """
        thx github.com/bomzheg/Shvatka
    """
    alembic_cfg = AlembicConfig("alembic.ini")

    alembic_cfg.set_main_option("script_location", "talkcorner/common/database/alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)

    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config: AlembicConfig):
    """
        thx github.com/bomzheg/Shvatka
    """
    upgrade(alembic_config, "head")
