import uuid
import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field

from talkcorner.common import dto
from talkcorner.common.types.common import Update


class TopicMessageValidators(BaseModel):
    body: str = Field(min_length=1, max_length=4096)


class TopicMessage(TopicMessageValidators):
    id: uuid.UUID

    topic_id: uuid.UUID

    created_at: dt.datetime

    @classmethod
    def from_dto(cls, topic_message: dto.TopicMessage) -> "TopicMessage":
        return TopicMessage(
            id=topic_message.id,
            topic_id=topic_message.topic_id,
            body=topic_message.body,
            created_at=topic_message.created_at
        )


class TopicMessageCreate(TopicMessageValidators):
    topic_id: uuid.UUID


class TopicMessageUpdate(TopicMessageValidators, Update):
    body: Optional[str] # type: ignore
