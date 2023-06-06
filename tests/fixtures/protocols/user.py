from typing import Protocol, Optional

from talkcorner.common import dto


class CreateUser(Protocol):

    async def __call__(self, password: Optional[str] = None) -> dto.User:
        pass
