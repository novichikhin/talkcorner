import datetime as dt
import uuid

from dataclasses import dataclass
from typing import Optional


@dataclass
class Forum:
    id: int

    title: str
    description: Optional[str]

    created_at: dt.datetime

    creator_id: uuid.UUID
