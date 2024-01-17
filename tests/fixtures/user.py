import random
import string
from typing import Optional

import pytest
from passlib.context import CryptContext

from talkcorner.exceptions.base import BaseAppException
from talkcorner.database.holder import DatabaseHolder
from talkcorner.schemas.user import User
from talkcorner.services.auth.security import get_password_hash
from tests.fixtures.protocols.user import CreateUser


@pytest.fixture(scope="function")
def create_user(holder: DatabaseHolder, crypt_context: CryptContext) -> CreateUser:

    async def create_user(
        *,
        identifier: Optional[str] = None,
        password: Optional[str] = None,
        email_verified: bool = True
    ) -> User:
        if not identifier:
            identifier = "".join(random.choice(string.ascii_uppercase) for _ in range(8))

        try:
            created_user = await holder.user.create(
                username=identifier,
                password=get_password_hash(crypt_context=crypt_context, password=password or identifier),
                email=f"{identifier}@ya.ru",
                email_verified=email_verified
            )
            await holder.commit()
        except BaseAppException as e:
            await holder.rollback()
            raise e

        return created_user

    return create_user
