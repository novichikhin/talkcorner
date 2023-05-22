import uuid
import datetime as dt

import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid6

from talkcorner.server.database.models.main import Base
from talkcorner.server.database.models.forum import Forum


class Topic(Base):
    __tablename__ = "topics"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)

    forum_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("forums.id"), nullable=False)

    title: so.Mapped[str] = so.mapped_column(nullable=False)
    body: so.Mapped[str] = so.mapped_column(nullable=False)

    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)

    forum: so.Mapped["Forum"] = so.relationship()
