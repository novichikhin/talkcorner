from talkcorner.server.api.api_v1.responses.common import Error


class SubforumNotFound(Error):
    detail: str = "Subforum not found"


class SubforumNotFoundOrNotCreator(Error):
    detail: str = "Subforum not found or you are not the creator of this subforum"


class ParentForumNotFoundOrNotCreator(Error):
    detail: str = "Parent forum not found or you are not the creator of this forum"


class ChildForumNotFoundOrNotCreator(Error):
    detail: str = "Child forum not found or you are not the creator of this forum"


class ParentChildForumsAlreadyExists(Error):
    detail: str = "Parent and child forum already exists"


class UnableCreateSubforum(Error):
    detail: str = "Unable to create subforum"


class UnableUpdateSubforum(Error):
    detail: str = "Unable to update subforum"
