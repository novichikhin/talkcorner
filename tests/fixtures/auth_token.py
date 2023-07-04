import uuid

import pytest
from fastapi import FastAPI

from talkcorner.common import types
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.core.auth import create_access_token, create_refresh_token
from tests.fixtures.protocols.auth_token import CreateAuthAccessToken, CreateAuthRefreshToken


@pytest.fixture(scope="function")
def create_auth_access_token(app: FastAPI) -> CreateAuthAccessToken:
    settings: types.Setting = app.dependency_overrides[SettingsMarker]()

    def create_auth_access_token(user_id: uuid.UUID) -> str:
        return create_access_token(payload={"user_id": str(user_id)}, settings=settings)

    return create_auth_access_token


@pytest.fixture(scope="function")
def create_auth_refresh_token(app: FastAPI) -> CreateAuthRefreshToken:
    settings: types.Setting = app.dependency_overrides[SettingsMarker]()

    def create_auth_refresh_token(user_id: uuid.UUID) -> str:
        return create_refresh_token(payload={"user_id": str(user_id)}, settings=settings)

    return create_auth_refresh_token
