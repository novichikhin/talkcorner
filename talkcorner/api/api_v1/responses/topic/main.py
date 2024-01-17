import uuid

from pydantic import BaseModel

from talkcorner.api.api_v1.responses.base import BaseResponse


class TopicNotFoundDetail(BaseModel):
    message: str = "Topic not found"
    topic_id: uuid.UUID


class TopicNotFound(BaseResponse):
    detail: TopicNotFoundDetail


class TopicNotUpdated(BaseResponse):
    detail: str = "Topic not updated: topic not found or you are not the creator of this topic"


class TopicNotDeleted(BaseResponse):
    detail: str = "Topic not deleted: topic not found or you are not the creator of this topic"
