import uuid
import datetime as dt
from typing import Optional

from pydantic import Field

from talkcorner.server.schemas.base import BaseSchema, BasePatch


class TopicMessageValidators(BaseSchema):
    body: str = Field(min_length=1, max_length=4096)


class TopicMessage(TopicMessageValidators):
    id: uuid.UUID

    topic_id: uuid.UUID

    created_at: dt.datetime

    creator_id: uuid.UUID


class TopicMessageCreate(TopicMessageValidators):
    topic_id: uuid.UUID


class TopicMessagePatch(TopicMessageValidators, BasePatch):
    body: Optional[str] = Field(default=None) # type: ignore
