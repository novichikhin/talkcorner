from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common.database import models
from talkcorner.common.database.repositories.main import Repository


class ForumRepository(Repository[models.Forum]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Forum, session=session)
