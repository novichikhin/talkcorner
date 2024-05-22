import uuid
from dataclasses import dataclass
from typing import Union, Dict, Any

from talkcorner.exceptions.base import BaseAppException


@dataclass(frozen=True)
class TopicMessageNotFoundError(BaseAppException):
    topic_message_id: uuid.UUID

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return {
            "message": "Topic message not found",
            "topic_message_id": self.topic_message_id,
        }


class TopicMessageNotPatchedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Topic message not updated: topic message not found or you are not the creator of this topic message"


class TopicMessageNotDeletedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Topic message not deleted: topic message not found or you are not the creator of this topic message"
