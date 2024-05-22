import uuid
import datetime as dt

import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid6

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.topic.main import Topic as TopicScheme


class Topic(BaseModel):
    __tablename__ = "topics"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)

    forum_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("forums.id", ondelete="CASCADE"), nullable=False
    )

    title: so.Mapped[str] = so.mapped_column(nullable=False)
    body: so.Mapped[str] = so.mapped_column(nullable=False)

    created_at: so.Mapped[dt.datetime] = so.mapped_column(
        nullable=False, default=dt.datetime.utcnow
    )

    creator_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def to_scheme(self) -> TopicScheme:
        return TopicScheme(
            id=self.id,
            forum_id=self.forum_id,
            title=self.title,
            body=self.body,
            created_at=self.created_at,
            creator_id=self.creator_id,
        )
