import uuid
from typing import Optional, Any

from pydantic import model_validator, Field

from talkcorner.server.schemas.base import BaseUpdate, BaseSchema


class SubforumValidators(BaseSchema):
    parent_forum_id: int
    child_forum_id: int

    @model_validator(mode="after")
    def model_validator_subforum(self) -> "SubforumValidators":
        if self.parent_forum_id == self.child_forum_id:
            raise ValueError("parent_forum_id should not be equal child_forum_id")
        return self


class Subforum(BaseSchema):
    id: int

    parent_forum_id: int
    child_forum_id: int

    creator_id: uuid.UUID


class SubforumCreate(SubforumValidators):
    parent_forum_id: int
    child_forum_id: int


class SubforumUpdate(SubforumValidators, BaseUpdate):
    parent_forum_id: Optional[int] = Field(default=None) # type: ignore
    child_forum_id: Optional[int] = Field(default=None) # type: ignore
