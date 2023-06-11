import datetime as dt
import uuid

from dataclasses import dataclass
from typing import Optional

from talkcorner.common.dto import User


@dataclass
class Forum:
    id: int

    title: str
    description: Optional[str]

    created_at: dt.datetime

    creator_id: uuid.UUID

    creator: Optional["User"]
