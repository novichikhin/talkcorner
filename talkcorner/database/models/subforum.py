import uuid

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from talkcorner.database.models.base import BaseModel
from talkcorner.schemas.subforum import Subforum as SubforumScheme


class Subforum(BaseModel):
    __tablename__ = "subforums"
    __table_args__ = (
        UniqueConstraint(
            "parent_forum_id", "child_forum_id", name="subforums_parent_child_forums"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    parent_forum_id: Mapped[int] = mapped_column(
        ForeignKey("forums.id", ondelete="CASCADE"), nullable=False
    )

    child_forum_id: Mapped[int] = mapped_column(
        ForeignKey("forums.id", ondelete="CASCADE"), nullable=False
    )

    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def to_scheme(self) -> SubforumScheme:
        return SubforumScheme(
            id=self.id,
            parent_forum_id=self.parent_forum_id,
            child_forum_id=self.child_forum_id,
            creator_id=self.creator_id,
        )
