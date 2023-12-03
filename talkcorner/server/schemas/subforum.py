import uuid
from typing import Optional

from pydantic import model_validator, Field

from talkcorner.server.schemas.base import BaseSchema, BasePatch


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


class SubforumPatch(BasePatch):
    parent_forum_id: Optional[int] = Field(default=None)
    child_forum_id: Optional[int] = Field(default=None)

    @model_validator(mode="after")
    def model_validator_subforum(self) -> "SubforumPatch":
        if self.parent_forum_id and self.child_forum_id and self.parent_forum_id == self.child_forum_id:
            raise ValueError("parent_forum_id should not be equal child_forum_id")
        return self
