import datetime as dt
from typing import Optional

import sqlalchemy.orm as so

from talkcorner.common import dto
from talkcorner.common.database.models.main import Base


class Forum(Base):
    __tablename__ = "forums"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str] = so.mapped_column(nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column()
    created_at: so.Mapped[dt.datetime] = so.mapped_column(nullable=False, default=dt.datetime.utcnow)

    def to_dto(self) -> dto.Forum:
        return dto.Forum(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at
        )
