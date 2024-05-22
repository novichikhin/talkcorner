from pydantic import BaseModel

from talkcorner.api.api_v1.responses.base import BaseResponse


class ForumNotFoundDetail(BaseModel):
    message: str = "Forum not found"
    forum_id: int


class ForumNotFound(BaseResponse):
    detail: ForumNotFoundDetail


class ForumNotCreatorDetail(BaseModel):
    message: str = "You are not the creator of this forum"
    forum_id: int


class ForumNotCreator(BaseResponse):
    detail: ForumNotCreatorDetail


class ForumNotUpdated(BaseResponse):
    detail: str = (
        "Forum not updated: forum not found or you are not the creator of this forum"
    )


class ForumNotDeleted(BaseResponse):
    detail: str = (
        "Forum not deleted: forum not found or you are not the creator of this forum"
    )
