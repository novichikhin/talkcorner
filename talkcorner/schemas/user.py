import uuid
from datetime import datetime
from typing import Optional

from pydantic import Field, EmailStr

from talkcorner.schemas.base import BaseSchema, BasePatch

USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH = 4, 24
PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH = 8, 64


class UserValidators(BaseSchema):
    username: str = Field(
        min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH
    )
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )


class User(UserValidators):
    id: uuid.UUID

    email: EmailStr
    email_token: uuid.UUID
    email_verified: bool

    created_at: datetime


class UserLogin(UserValidators):
    pass


class UserCreate(UserValidators):
    email: EmailStr


class UserPatch(BasePatch):
    password: Optional[str] = Field(
        default=None, min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )
