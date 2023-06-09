from typing import Protocol, Optional

from talkcorner.common import dto


class CreateUser(Protocol):

    async def __call__(
            self,
            *,
            identifier: Optional[str] = None,
            password: Optional[str] = None,
            email_verified: bool = True
    ) -> dto.User:
        pass
