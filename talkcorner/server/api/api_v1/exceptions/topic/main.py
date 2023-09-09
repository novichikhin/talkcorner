import uuid
from dataclasses import dataclass
from typing import Union, Dict, Any

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException


@dataclass(frozen=True)
class TopicNotFoundError(BaseAppException):
    topic_id: uuid.UUID

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return {
            "message": "Topic not found",
            "topic_id": self.topic_id
        }


class TopicNotPatchedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Topic not updated: topic not found or you are not the creator of this topic"


class TopicNotDeletedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Topic not deleted: topic not found or you are not the creator of this topic"
