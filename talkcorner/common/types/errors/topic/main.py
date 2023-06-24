from talkcorner.common.types.errors.common import Error


class TopicNotFound(Error):
    detail: str = "Topic not found"


class TopicNotFoundOrNotCreator(Error):
    detail: str = "Topic not found or you are not the creator of this topic"


class UnableCreateTopic(Error):
    detail: str = "Unable to create topic"


class UnableUpdateTopic(Error):
    detail: str = "Unable to update topic"
