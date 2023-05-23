import datetime as dt
import uuid

from dataclasses import dataclass


@dataclass
class User:
    id: uuid.UUID

    username: str
    password: str
    email: str
    email_verified: bool

    created_at: dt.datetime
