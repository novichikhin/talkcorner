import datetime as dt
import uuid
import sqlalchemy as sa

from typing import Optional

import sqlalchemy.orm as so

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.forum import Forum as ForumScheme


class Forum(BaseModel):
    __tablename__ = "forums"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str] = so.mapped_column(nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column()
    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)

    creator_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    def to_scheme(self) -> ForumScheme:
        return ForumScheme(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            creator_id=self.creator_id
        )
