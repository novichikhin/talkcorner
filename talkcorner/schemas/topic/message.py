import uuid
import datetime as dt
from typing import Optional

from pydantic import Field

from talkcorner.schemas.base import BaseSchema, BasePatch

BODY_MIN_LENGTH, BODY_MAX_LENGTH = 1, 4096


class TopicMessageValidators(BaseSchema):
    body: str = Field(min_length=BODY_MIN_LENGTH, max_length=BODY_MAX_LENGTH)


class TopicMessage(TopicMessageValidators):
    id: uuid.UUID

    topic_id: uuid.UUID

    created_at: dt.datetime

    creator_id: uuid.UUID


class TopicMessageCreate(TopicMessageValidators):
    topic_id: uuid.UUID


class TopicMessagePatch(BasePatch):
    body: Optional[str] = Field(
        default=None,
        min_length=BODY_MIN_LENGTH,
        max_length=BODY_MAX_LENGTH
    )
