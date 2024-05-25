import uuid
from datetime import datetime

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.forum import Forum as ForumScheme


class Forum(BaseModel):
    __tablename__ = "forums"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )

    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def to_scheme(self) -> ForumScheme:
        return ForumScheme(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            creator_id=self.creator_id,
        )
