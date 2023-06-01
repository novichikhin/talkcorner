import pytest

from talkcorner.common import dto
from talkcorner.common.database.holder import DatabaseHolder
from tests.fixtures.protocols.user import CreateUser


@pytest.fixture(scope="function")
def create_user(holder: DatabaseHolder) -> CreateUser:

    async def create_user(
            username: str,
            hashed_password: str,
            email: str
    ) -> dto.User:
        user = await holder.user.create(
            username=username,
            password=hashed_password,
            email=email
        )

        if not user:
            raise RuntimeError("Unable to create user")

        return user

    return create_user
