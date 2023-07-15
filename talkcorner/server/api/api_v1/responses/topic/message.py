from talkcorner.server.api.api_v1.responses.common import Error


class TopicMessageNotFound(Error):
    detail: str = "Topic message not found"


class TopicMessageNotFoundOrNotCreator(Error):
    detail: str = "Topic message not found or you are not the creator of this topic message"


class UnableCreateTopicMessage(Error):
    detail: str = "Unable to create topic message"


class UnableUpdateTopicMessage(Error):
    detail: str = "Unable to update topic message"
