from typing import Protocol

from talkcorner.common import dto


class CreateUser(Protocol):

    async def __call__(
            self,
            username: str,
            hashed_password: str,
            email: str
    ) -> dto.User:
        pass
