import uuid
import datetime as dt

import sqlalchemy.orm as so

import uuid6

from talkcorner.server.database.models.main import Base


class User(Base):
    __tablename__ = "users"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)
    username: so.Mapped[str] = so.mapped_column(nullable=False, unique=True)
    password: so.Mapped[str] = so.mapped_column(nullable=False)
    email: so.Mapped[str] = so.mapped_column(nullable=False, unique=True)
    email_verified: so.Mapped[bool] = so.mapped_column(nullable=False, default=False)
    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)
