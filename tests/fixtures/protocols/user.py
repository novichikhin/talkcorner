from typing import Protocol, Optional

from talkcorner.schemas.user import User


class CreateUser(Protocol):

    async def __call__(
            self,
            *,
            identifier: Optional[str] = None,
            password: Optional[str] = None,
            email_verified: bool = True
    ) -> User:
        pass
