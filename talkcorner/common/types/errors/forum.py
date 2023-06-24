from talkcorner.common.types.errors.common import Error


class ForumNotFound(Error):
    detail: str = "Forum not found"


class ForumNotFoundOrNotCreator(Error):
    detail: str = "Forum not found or you are not the creator of this forum"


class UnableUpdateForum(Error):
    detail: str = "Unable to update forum"
