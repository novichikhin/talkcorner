import random
import string
from typing import Optional

import pytest
from passlib.context import CryptContext

from talkcorner.common import dto
from talkcorner.common.database.holder import DatabaseHolder
from talkcorner.server.core.security import get_password_hash
from tests.fixtures.protocols.user import CreateUser


@pytest.fixture(scope="function")
def create_user(holder: DatabaseHolder, crypt_context: CryptContext) -> CreateUser:

    async def create_user(password: Optional[str] = None) -> dto.User:
        random_indetifier = "".join(random.choice(string.ascii_uppercase) for _ in range(8))

        user = await holder.user.create(
            username=random_indetifier,
            password=get_password_hash(crypt_context=crypt_context, password=password or random_indetifier),
            email=f"{random_indetifier}@ya.ru"
        )

        if not user:
            raise RuntimeError("Unable to create user")

        return user

    return create_user
