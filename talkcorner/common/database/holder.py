from sqlalchemy.ext.asyncio import AsyncSession

from talkcorner.common.database.repositories.user import UserRepository


class DatabaseHolder:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.user = UserRepository(session=session)
