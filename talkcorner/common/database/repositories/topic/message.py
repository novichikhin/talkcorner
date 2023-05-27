from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class TopicMessageRepository(Repository[models.TopicMessage]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.TopicMessage, session=session)
