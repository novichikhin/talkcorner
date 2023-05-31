import datetime as dt
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from talkcorner.common import dto


class ForumValidators(BaseModel):
    title: str = Field(min_length=10, max_length=64)
    description: Optional[str] = Field(min_length=10, max_length=256)


class Forum(ForumValidators):
    id: int

    created_at: dt.datetime

    creator_id: uuid.UUID

    @classmethod
    def from_dto(cls, forum: dto.Forum) -> "Forum":
        return Forum(
            id=forum.id,
            title=forum.title,
            description=forum.description,
            created_at=forum.created_at,
            creator_id=forum.creator_id
        )


class ForumCreate(ForumValidators):
    pass


class ForumUpdate(ForumValidators):
    title: Optional[str] # type: ignore
    description: Optional[str]
