import sqlalchemy as sa
import sqlalchemy.orm as so

from talkcorner.common import dto
from talkcorner.common.database.models.main import Base
from talkcorner.common.database.models.forum import Forum


class Subforum(Base):
    __tablename__ = "subforums"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    parent_forum_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("forums.id"), nullable=False)
    child_forum_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("forums.id"), nullable=False)

    parent_forum: so.Mapped["Forum"] = so.relationship(foreign_keys="Subforum.parent_forum_id")
    child_forum: so.Mapped["Forum"] = so.relationship(foreign_keys="Subforum.child_forum_id")

    def to_dto(
            self,
            parent_forum: dto.Forum,
            child_forum: dto.Forum
    ) -> dto.Subforum:
        return dto.Subforum(
            id=self.id,
            parent_forum_id=self.parent_forum_id,
            child_forum_id=self.child_forum_id,
            parent_forum=parent_forum,
            child_forum=child_forum
        )
