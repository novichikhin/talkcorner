import uuid
import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from talkcorner.common import dto


class UserValidators(BaseModel):
    username: str = Field(min_length=4, max_length=24)
    password: str = Field(min_length=8, max_length=64)


class User(UserValidators):
    id: uuid.UUID

    email: EmailStr
    email_verified: bool

    created_at: dt.datetime

    @classmethod
    def from_dto(cls, user: dto.User) -> "User":
        return User(
            id=user.id,
            username=user.username,
            password=user.password,
            email=EmailStr(user.email),
            email_verified=user.email_verified,
            created_at=user.created_at
        )


class UserLogin(UserValidators):
    pass


class UserCreate(UserValidators):
    email: EmailStr


class UserUpdate(UserValidators):
    password: Optional[str] # type: ignore
