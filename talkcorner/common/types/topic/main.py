import uuid
import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field

from talkcorner.common import dto
from talkcorner.common.types.common import Update


class TopicValidators(BaseModel):
    title: str = Field(min_length=10, max_length=48)
    body: str = Field(min_length=1, max_length=4096)


class Topic(TopicValidators):
    id: uuid.UUID

    forum_id: int

    created_at: dt.datetime

    @classmethod
    def from_dto(cls, topic: dto.Topic) -> "Topic":
        return Topic(
            id=topic.id,
            forum_id=topic.forum_id,
            title=topic.title,
            body=topic.body,
            created_at=topic.created_at
        )


class TopicCreate(TopicValidators):
    forum_id: int


class TopicUpdate(TopicValidators, Update):
    forum_id: Optional[int] # type: ignore
    title: Optional[str] # type: ignore
    body: Optional[str] # type: ignore
