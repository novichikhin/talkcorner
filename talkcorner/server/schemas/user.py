import uuid
import datetime as dt
from typing import Optional

from pydantic import Field, EmailStr

from talkcorner.server.schemas.base import BaseUpdate, BaseSchema


class UserValidators(BaseSchema):
    username: str = Field(min_length=4, max_length=24)
    password: str = Field(min_length=8, max_length=64)


class User(UserValidators):
    id: uuid.UUID

    email: EmailStr
    email_token: uuid.UUID
    email_verified: bool

    created_at: dt.datetime


class UserLogin(UserValidators):
    pass


class UserCreate(UserValidators):
    email: EmailStr


class UserUpdate(UserValidators, BaseUpdate):
    password: Optional[str] = Field(default=None) # type: ignore
