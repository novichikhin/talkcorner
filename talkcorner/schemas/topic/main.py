import uuid
from datetime import datetime
from typing import Optional

from pydantic import Field

from talkcorner.schemas.base import BaseSchema, BasePatch

TITLE_MIN_LENGTH, TITLE_MAX_LENGTH = 10, 48
BODY_MIN_LENGTH, BODY_MAX_LENGTH = 1, 4096


class TopicValidators(BaseSchema):
    title: str = Field(min_length=TITLE_MIN_LENGTH, max_length=TITLE_MAX_LENGTH)
    body: str = Field(min_length=BODY_MIN_LENGTH, max_length=BODY_MAX_LENGTH)


class Topic(TopicValidators):
    id: uuid.UUID

    forum_id: int

    created_at: datetime

    creator_id: uuid.UUID


class TopicCreate(TopicValidators):
    forum_id: int


class TopicPatch(BasePatch):
    forum_id: Optional[int] = Field(default=None)

    title: Optional[str] = Field(
        default=None, min_length=TITLE_MIN_LENGTH, max_length=TITLE_MAX_LENGTH
    )

    body: Optional[str] = Field(
        default=None, min_length=BODY_MIN_LENGTH, max_length=BODY_MAX_LENGTH
    )
