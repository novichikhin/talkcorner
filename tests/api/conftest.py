import os

import sqlalchemy as sa
import pytest_asyncio

from typing import Generator

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import URL, make_url
from sqlalchemy.orm import sessionmaker, close_all_sessions
from testcontainers.postgres import PostgresContainer

from talkcorner.common.settings.environments.base import AppEnvTypes
from talkcorner.common.settings.main import get_app_settings
from talkcorner.server.api.api_v1.dependencies.database import DatabaseSessionMarker
from talkcorner.server.api.api_v1.dependencies.nats import NatsJetStreamMarker
from talkcorner.server.api.setup import register_app
from talkcorner.server.database.models.base import BaseModel
from tests.fixtures.conftest import holder, crypt_context, nats_mock # noqa: F401
from tests.fixtures.user import create_user # noqa: F401
from tests.fixtures.auth_token import create_auth_access_token # noqa: F401
from tests.mocks.nats import JetStreamContextMock


@pytest.fixture(scope="session", autouse=True)
def app(postgres_url: str) -> FastAPI:
    url: URL = make_url(postgres_url)
    settings = get_app_settings(app_env=AppEnvTypes.dev).model_copy(
        update={
            "pg_driver": "asyncpg",
            "pg_host": url.host,
            "pg_port": url.port,
            "pg_user": url.username,
            "pg_password": url.password,
            "pg_db": url.database
        }
    )

    return register_app(settings=settings)


@pytest.fixture(scope="session", autouse=True)
def nats(app: FastAPI, nats_mock: JetStreamContextMock):
    app.dependency_overrides.update(
        {
            NatsJetStreamMarker: lambda: nats_mock
        }
    )


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(session_factory: sessionmaker) -> None:
    async with session_factory() as session:
        for table in BaseModel.metadata.tables:
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
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)

    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config: AlembicConfig):
    """
        thx github.com/bomzheg/Shvatka
    """
    upgrade(alembic_config, "head")
