import uuid
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from talkcorner.common import dto
from talkcorner.common.database.models import User
from talkcorner.common.database.models.main import Base
from talkcorner.common.database.models.forum import Forum


class Subforum(Base):
    __tablename__ = "subforums"
    __table_args__ = (sa.UniqueConstraint("parent_forum_id", "child_forum_id", name="subforums_parent_child_forums"),)

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    parent_forum_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("forums.id"), nullable=False)
    child_forum_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("forums.id"), nullable=False)

    creator_id: so.Mapped[uuid.UUID] = so.mapped_column(sa.ForeignKey("users.id"), nullable=False)

    parent_forum: so.Mapped["Forum"] = so.relationship(foreign_keys="Subforum.parent_forum_id")
    child_forum: so.Mapped["Forum"] = so.relationship(foreign_keys="Subforum.child_forum_id")

    creator: so.Mapped["User"] = so.relationship()

    def to_dto(
            self,
            parent_forum: Optional[dto.Forum] = None,
            child_forum: Optional[dto.Forum] = None,
            creator: Optional[dto.User] = None
    ) -> dto.Subforum:
        return dto.Subforum(
            id=self.id,
            parent_forum_id=self.parent_forum_id,
            child_forum_id=self.child_forum_id,
            creator_id=self.creator_id,
            parent_forum=parent_forum,
            child_forum=child_forum,
            creator=creator
        )
