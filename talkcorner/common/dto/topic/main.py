import datetime as dt
import uuid

from dataclasses import dataclass
from typing import Optional

from talkcorner.common.dto.forum import Forum


@dataclass
class Topic:
    id: uuid.UUID

    forum_id: int

    title: str
    body: str

    created_at: dt.datetime

    forum: Optional["Forum"] = None
