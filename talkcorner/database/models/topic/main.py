import uuid
from datetime import datetime

import uuid6
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.topic.main import Topic as TopicScheme


class Topic(BaseModel):
    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid6.uuid7)

    forum_id: Mapped[int] = mapped_column(
        ForeignKey("forums.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )

    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
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
