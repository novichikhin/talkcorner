from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseProvider:

    def __init__(self, session: AsyncSession):
        self.session = session
