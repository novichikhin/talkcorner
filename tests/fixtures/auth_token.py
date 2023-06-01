import uuid

import pytest
from fastapi import FastAPI

from talkcorner.common import types
from talkcorner.server.api.api_v1.dependencies.settings import SettingsMarker
from talkcorner.server.core.auth import create_access_token
from tests.fixtures.protocols.auth_token import CreateAuthToken


@pytest.fixture(scope="function")
def create_auth_token(app: FastAPI) -> CreateAuthToken:
    settings: types.Setting = app.dependency_overrides[SettingsMarker]()

    def create_auth_token(user_id: uuid.UUID) -> str:
        return create_access_token(payload={"user_id": str(user_id)}, settings=settings)

    return create_auth_token
