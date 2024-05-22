from pydantic import BaseModel

from talkcorner.api.api_v1.responses.base import BaseResponse


class SubforumNotFoundDetail(BaseModel):
    message: str = "Subforum not found"
    subforum_id: int


class SubforumNotFound(BaseResponse):
    detail: SubforumNotFoundDetail


class SubforumNotUpdated(BaseResponse):
    detail: str = (
        "Subforum not updated: subforum not found or you are not the creator of this subforum"
    )


class SubforumNotDeleted(BaseResponse):
    detail: str = (
        "Subforum not deleted: subforum not found or you are not the creator of this subforum"
    )


class ParentChildForumsAlreadyExists(BaseResponse):
    detail: str = "Parent and child forum already exists"
