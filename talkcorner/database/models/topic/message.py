import uuid
import datetime as dt

import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid6

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.topic.message import TopicMessage as TopicMessageScheme


class TopicMessage(BaseModel):
    __tablename__ = "topic_messages"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)

    topic_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    body: so.Mapped[str] = so.mapped_column(nullable=False)

    created_at: so.Mapped[dt.datetime] = so.mapped_column(
        nullable=False, default=dt.datetime.utcnow
    )

    creator_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def to_scheme(self) -> TopicMessageScheme:
        return TopicMessageScheme(
            id=self.id,
            topic_id=self.topic_id,
            body=self.body,
            created_at=self.created_at,
            creator_id=self.creator_id,
        )
