import uuid

import pytest
from fastapi import FastAPI

from talkcorner.common.settings.app import AppSettings
from talkcorner.server.api.api_v1.dependencies.setting import SettingsMarker
from talkcorner.server.services.auth.token import create_access_token, create_refresh_token
from tests.fixtures.protocols.auth_token import CreateAuthAccessToken, CreateAuthRefreshToken


@pytest.fixture(scope="function")
def create_auth_access_token(app: FastAPI) -> CreateAuthAccessToken:
    settings: AppSettings = app.dependency_overrides[SettingsMarker]()

    def create_auth_access_token(user_id: uuid.UUID) -> str:
        return create_access_token(
            payload={"user_id": str(user_id)},
            secret_key=settings.authorize_access_token_secret_key,
            expire_minutes=settings.authorize_access_token_expire_minutes
        )

    return create_auth_access_token


@pytest.fixture(scope="function")
def create_auth_refresh_token(app: FastAPI) -> CreateAuthRefreshToken:
    settings: AppSettings = app.dependency_overrides[SettingsMarker]()

    def create_auth_refresh_token(user_id: uuid.UUID) -> str:
        return create_refresh_token(
            payload={"user_id": str(user_id)},
            secret_key=settings.authorize_refresh_token_secret_key,
            expire_minutes=settings.authorize_refresh_token_expire_minutes
        )

    return create_auth_refresh_token
