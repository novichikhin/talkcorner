from typing import Optional

from pydantic import BaseModel

from talkcorner.common import dto


class Subforum(BaseModel):
    id: int

    parent_forum_id: int
    child_forum_id: int

    @classmethod
    def from_dto(cls, subforum: dto.Subforum) -> "Subforum":
        return Subforum(
            id=subforum.id,
            parent_forum_id=subforum.parent_forum_id,
            child_forum_id=subforum.child_forum_id
        )


class SubforumCreate(BaseModel):
    parent_forum_id: int
    child_forum_id: int


class SubforumUpdate(BaseModel):
    parent_forum_id: Optional[int]
    child_forum_id: Optional[int]
