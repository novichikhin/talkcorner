import uuid
import datetime as dt

import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid6

from talkcorner.common import dto
from talkcorner.common.database.models.main import Base
from talkcorner.common.database.models.topic.main import Topic


class TopicMessage(Base):
    __tablename__ = "topic_messages"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)

    topic_id: so.Mapped[uuid.UUID] = so.mapped_column(sa.ForeignKey("topics.id"), nullable=False)

    body: so.Mapped[str] = so.mapped_column(nullable=False)

    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)

    topic: so.Mapped["Topic"] = so.relationship()

    def to_dto(self, topic: dto.Topic) -> dto.TopicMessage:
        return dto.TopicMessage(
            id=self.id,
            topic_id=self.topic_id,
            body=self.body,
            created_at=self.created_at,
            topic=topic
        )
