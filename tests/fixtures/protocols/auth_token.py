import uuid
from typing import Protocol


class CreateAuthToken(Protocol):

    def __call__(self, user_id: uuid.UUID) -> str:
        pass
