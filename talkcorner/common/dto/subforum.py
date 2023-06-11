import uuid

from dataclasses import dataclass
from typing import Optional

from talkcorner.common.dto import User
from talkcorner.common.dto.forum import Forum


@dataclass
class Subforum:
    id: int

    parent_forum_id: int
    child_forum_id: int

    creator_id: uuid.UUID

    parent_forum: Optional["Forum"] = None
    child_forum: Optional["Forum"] = None
    creator: Optional["User"] = None
