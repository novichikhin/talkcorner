from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common.database.repositories.forum import ForumRepository
from talkcorner.common.database.repositories.subforum import SubforumRepository
from talkcorner.common.database.repositories.topic.main import TopicRepository
from talkcorner.common.database.repositories.topic.message import TopicMessageRepository
from talkcorner.common.database.repositories.user import UserRepository


class DatabaseHolder:

    def __init__(self, session: AsyncSession):
        self.user = UserRepository(session=session)
        self.forum = ForumRepository(session=session)
        self.subforum = SubforumRepository(session=session)
        self.topic = TopicRepository(session=session)
        self.topic_message = TopicMessageRepository(session=session)
