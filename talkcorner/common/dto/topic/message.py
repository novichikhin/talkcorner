import datetime as dt
import uuid

from dataclasses import dataclass
from typing import Optional

from talkcorner.common.dto import User
from talkcorner.common.dto.topic.main import Topic


@dataclass
class TopicMessage:
    id: uuid.UUID

    topic_id: uuid.UUID

    body: str

    created_at: dt.datetime

    creator_id: uuid.UUID

    topic: Optional["Topic"] = None
    creator: Optional["User"] = None
