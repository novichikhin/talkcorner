import uuid

from pydantic import BaseModel

from talkcorner.server.api.api_v1.responses.base import BaseResponse


class TopicMessageNotFoundDetail(BaseModel):
    message: str = "Topic message not found"
    topic_message_id: uuid.UUID


class TopicMessageNotFound(BaseResponse):
    detail: TopicMessageNotFoundDetail


class TopicMessageNotUpdated(BaseResponse):
    detail: str = "Topic message not updated: topic message not found or you are not the creator of this topic message"


class TopicMessageNotDeleted(BaseResponse):
    detail: str = "Topic message not deleted: topic message not found or you are not the creator of this topic message"
