from talkcorner.common.types.errors.common import Validation, SomethingWentWrong
from talkcorner.common.types.errors.user import (
    NotValidateCredentials,
    AuthenticationUserNotFound,
    UserNotFound,
    WrongUsernameOrPassword,
    EmailAlreadyExists,
    UsernameAlreadyExists,
    UnableCreateUser
)
from talkcorner.common.types.errors.forum import (
    ForumNotFound,
    ForumNotFoundOrNotCreator,
    UnableUpdateForum
)
from talkcorner.common.types.errors.subforum import (
    SubforumNotFound,
    SubforumNotFoundOrNotCreator,
    ParentForumNotFoundOrNotCreator,
    ChildForumNotFoundOrNotCreator,
    ParentChildForumsAlreadyExists,
    UnableCreateSubforum,
    UnableUpdateSubforum
)
from talkcorner.common.types.errors.topic.main import (
    TopicNotFound,
    TopicNotFoundOrNotCreator,
    UnableCreateTopic,
    UnableUpdateTopic
)
from talkcorner.common.types.errors.topic.message import (
    TopicMessageNotFound,
    TopicMessageNotFoundOrNotCreator,
    UnableCreateTopicMessage,
    UnableUpdateTopicMessage
)
