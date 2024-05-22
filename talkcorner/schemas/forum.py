import datetime as dt
import uuid
from typing import Optional

from pydantic import Field

from talkcorner.schemas.base import BaseSchema, BasePatch

TITLE_MIN_LENGTH, TITLE_MAX_LENGTH = 10, 64
DESCRIPTION_MIN_LENGTH, DESCRIPTION_MAX_LENGTH = 10, 256


class ForumValidators(BaseSchema):
    title: str = Field(min_length=TITLE_MIN_LENGTH, max_length=TITLE_MAX_LENGTH)
    description: Optional[str] = Field(
        min_length=DESCRIPTION_MIN_LENGTH, max_length=DESCRIPTION_MAX_LENGTH
    )


class Forum(ForumValidators):
    id: int

    created_at: dt.datetime

    creator_id: uuid.UUID


class ForumCreate(ForumValidators):
    pass


class ForumPatch(BasePatch):
    title: Optional[str] = Field(
        default=None, min_length=TITLE_MIN_LENGTH, max_length=TITLE_MAX_LENGTH
    )

    description: Optional[str] = Field(
        default=None,
        min_length=DESCRIPTION_MIN_LENGTH,
        max_length=DESCRIPTION_MAX_LENGTH,
    )
