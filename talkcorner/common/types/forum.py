import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field

from talkcorner.common import dto


class ForumValidators(BaseModel):
    title: str = Field(min_length=10, max_length=64)
    description: Optional[str] = Field(min_length=10, max_length=256)


class Forum(ForumValidators):
    id: int

    created_at: dt.datetime

    @classmethod
    def from_dto(cls, forum: dto.Forum) -> "Forum":
        return Forum(
            id=forum.id,
            title=forum.title,
            description=forum.description,
            created_at=forum.created_at
        )


class ForumCreate(ForumValidators):
    pass


class ForumUpdate(ForumValidators):
    title: Optional[str] # type: ignore
    description: Optional[str]
