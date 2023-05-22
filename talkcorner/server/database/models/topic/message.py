import uuid
import datetime as dt

import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid6

from talkcorner.server.database.models.main import Base
from talkcorner.server.database.models.topic.main import Topic


class TopicMessage(Base):
    __tablename__ = "topic_messages"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)

    topic_id: so.Mapped[uuid.UUID] = so.mapped_column(sa.ForeignKey("topics.id"), nullable=False)

    body: so.Mapped[str] = so.mapped_column(nullable=False)

    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)

    topic: so.Mapped["Topic"] = so.relationship()
