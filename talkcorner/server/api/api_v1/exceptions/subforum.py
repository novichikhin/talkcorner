from dataclasses import dataclass
from typing import Union, Dict, Any

from talkcorner.server.api.api_v1.exceptions.base import BaseAppException


@dataclass(frozen=True)
class SubforumNotFoundError(BaseAppException):
    subforum_id: int

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return {
            "message": "Subforum not found",
            "subforum_id": self.subforum_id
        }


class SubforumNotUpdatedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Subforum not updated: subforum not found or you are not the creator of this subforum"


class SubforumNotDeletedError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Subforum not deleted: subforum not found or you are not the creator of this subforum"


class ParentChildForumsAlreadyExistsError(BaseAppException):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        return "Parent and child forum already exists"
