import datetime as dt

from dataclasses import dataclass
from typing import Optional


@dataclass
class Forum:
    id: int

    title: str
    description: Optional[str]

    created_at: dt.datetime
