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

    async def create_user(
            *,
            identifier: Optional[str] = None,
            password: Optional[str] = None,
            email_verified: bool = True
    ) -> dto.User:
        if not identifier:
            identifier = "".join(random.choice(string.ascii_uppercase) for _ in range(8))

        user = await holder.user.create(
            username=identifier,
            password=get_password_hash(crypt_context=crypt_context, password=password or identifier),
            email=f"{identifier}@ya.ru",
            email_verified=email_verified
        )

        return user

    return create_user
