import uuid
from datetime import datetime

import uuid6
from sqlalchemy.orm import Mapped, mapped_column

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.user import User as UserScheme


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid6.uuid7)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    email_token: Mapped[uuid.UUID] = mapped_column(unique=True, default=uuid6.uuid7)
    email_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )

    def to_scheme(self) -> UserScheme:
        return UserScheme(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email,
            email_token=self.email_token,
            email_verified=self.email_verified,
            created_at=self.created_at,
        )
