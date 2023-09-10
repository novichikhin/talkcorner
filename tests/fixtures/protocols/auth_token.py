import uuid
from typing import Protocol


class CreateAuthAccessToken(Protocol):

    def __call__(self, user_id: uuid.UUID) -> str:
        pass
