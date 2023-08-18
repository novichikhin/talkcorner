from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.server.database.repositories.forum import ForumRepository
from talkcorner.server.database.repositories.subforum import SubforumRepository
from talkcorner.server.database.repositories.topic.main import TopicRepository
from talkcorner.server.database.repositories.topic.message import TopicMessageRepository
from talkcorner.server.database.repositories.user import UserRepository


class DatabaseHolder:

    def __init__(self, session: AsyncSession):
        self._session = session

        self.user = UserRepository(session=session)
        self.forum = ForumRepository(session=session)
        self.subforum = SubforumRepository(session=session)
        self.topic = TopicRepository(session=session)
        self.topic_message = TopicMessageRepository(session=session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
