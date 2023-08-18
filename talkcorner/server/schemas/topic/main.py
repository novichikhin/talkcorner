import uuid
import datetime as dt
from typing import Optional

from pydantic import Field

from talkcorner.server.schemas.base import BaseUpdate, BaseSchema


class TopicValidators(BaseSchema):
    title: str = Field(min_length=10, max_length=48)
    body: str = Field(min_length=1, max_length=4096)


class Topic(TopicValidators):
    id: uuid.UUID

    forum_id: int

    created_at: dt.datetime

    creator_id: uuid.UUID


class TopicCreate(TopicValidators):
    forum_id: int


class TopicUpdate(TopicValidators, BaseUpdate):
    forum_id: Optional[int] = Field(default=None) # type: ignore
    title: Optional[str] = Field(default=None) # type: ignore
    body: Optional[str] = Field(default=None) # type: ignore
