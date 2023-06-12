import uuid
import datetime as dt
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid6

from talkcorner.common import dto
from talkcorner.common.database.models import User
from talkcorner.common.database.models.main import Base
from talkcorner.common.database.models.forum import Forum


class Topic(Base):
    __tablename__ = "topics"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)

    forum_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("forums.id", ondelete="CASCADE"), nullable=False)

    title: so.Mapped[str] = so.mapped_column(nullable=False)
    body: so.Mapped[str] = so.mapped_column(nullable=False)

    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)

    creator_id: so.Mapped[uuid.UUID] = so.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    forum: so.Mapped["Forum"] = so.relationship()
    creator: so.Mapped["User"] = so.relationship()

    def to_dto(
            self,
            forum: Optional[dto.Forum] = None,
            creator: Optional[dto.User] = None
    ) -> dto.Topic:
        return dto.Topic(
            id=self.id,
            forum_id=self.forum_id,
            title=self.title,
            body=self.body,
            created_at=self.created_at,
            creator_id=self.creator_id,
            forum=forum,
            creator=creator
        )
