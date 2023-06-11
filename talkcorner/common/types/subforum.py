import uuid
from typing import Optional, Any

from pydantic import BaseModel, root_validator

from talkcorner.common import dto
from talkcorner.common.types.common import Update


class SubforumValidators(BaseModel):
    parent_forum_id: int
    child_forum_id: int

    @root_validator
    def root_validator_subforum(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values["parent_forum_id"] == values["child_forum_id"]:
            raise ValueError("parent_forum_id should not be equal child_forum_id")
        return values


class Subforum(BaseModel):
    id: int

    parent_forum_id: int
    child_forum_id: int

    creator_id: uuid.UUID

    @classmethod
    def from_dto(cls, subforum: dto.Subforum) -> "Subforum":
        return Subforum(
            id=subforum.id,
            parent_forum_id=subforum.parent_forum_id,
            child_forum_id=subforum.child_forum_id,
            creator_id=subforum.creator_id
        )


class SubforumCreate(SubforumValidators):
    parent_forum_id: int
    child_forum_id: int


class SubforumUpdate(SubforumValidators, Update):
    parent_forum_id: Optional[int] # type: ignore
    child_forum_id: Optional[int] # type: ignore
