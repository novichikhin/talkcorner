from dataclasses import dataclass
from typing import Union, Dict, Any

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException


@dataclass(frozen=True)
class ForumNotFoundError(BaseAppException):
    forum_id: int

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return {
            "message": "Forum not found",
            "forum_id": self.forum_id
        }


@dataclass(frozen=True)
class ForumNotCreatorError(BaseAppException):
    forum_id: int

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return {
            "message": "You are not the creator of this forum",
            "forum_id": self.forum_id
        }


class ForumNotPatchedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Forum not updated: forum not found or you are not the creator of this forum"


class ForumNotDeletedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Forum not deleted: forum not found or you are not the creator of this forum"
