import uuid
from datetime import datetime

import uuid6
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.topic.message import TopicMessage as TopicMessageScheme


class TopicMessage(BaseModel):
    __tablename__ = "topic_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid6.uuid7)

    topic_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    body: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )

    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def to_scheme(self) -> TopicMessageScheme:
        return TopicMessageScheme(
            id=self.id,
            topic_id=self.topic_id,
            body=self.body,
            created_at=self.created_at,
            creator_id=self.creator_id,
        )
