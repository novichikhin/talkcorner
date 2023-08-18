import datetime as dt
import uuid
from typing import Optional

from pydantic import Field

from talkcorner.server.schemas.base import BaseUpdate, BaseSchema


class ForumValidators(BaseSchema):
    title: str = Field(min_length=10, max_length=64)
    description: Optional[str] = Field(min_length=10, max_length=256)


class Forum(ForumValidators):
    id: int

    created_at: dt.datetime

    creator_id: uuid.UUID


class ForumCreate(ForumValidators):
    pass


class ForumUpdate(ForumValidators, BaseUpdate):
    title: Optional[str] = Field(default=None) # type: ignore
    description: Optional[str] = Field(default=None) # type: ignore
