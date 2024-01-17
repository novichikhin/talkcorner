import uuid
import datetime as dt

import sqlalchemy.orm as so

import uuid6

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.user import User as UserScheme


class User(BaseModel):
    __tablename__ = "users"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)
    username: so.Mapped[str] = so.mapped_column(nullable=False, unique=True)
    password: so.Mapped[str] = so.mapped_column(nullable=False)
    email: so.Mapped[str] = so.mapped_column(nullable=False, unique=True)
    email_token: so.Mapped[uuid.UUID] = so.mapped_column(unique=True, default=uuid6.uuid7)
    email_verified: so.Mapped[bool] = so.mapped_column(nullable=False, default=False)
    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)

    def to_scheme(self) -> UserScheme:
        return UserScheme(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email,
            email_token=self.email_token,
            email_verified=self.email_verified,
            created_at=self.created_at
        )
