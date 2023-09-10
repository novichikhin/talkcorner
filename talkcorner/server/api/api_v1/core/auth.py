from typing import Callable, Awaitable

from fastapi import Header, Depends

from talkcorner.common.settings.environments.app import AppSettings
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.dependencies.setting import SettingsMarker
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.user import User
from talkcorner.server.services.auth.main import authenticate_user


def api_authenticate_user(
    check_email_verified: bool = True
) -> Callable[[str, DatabaseHolder, AppSettings], Awaitable[User]]:

    async def api_authenticate_user(
            authorization: str = Header(alias="Authorization"),
            holder: DatabaseHolder = Depends(DatabaseHolderMarker),
            settings: AppSettings = Depends(SettingsMarker)
    ) -> User:
        return await authenticate_user(
            authorization=authorization,
            check_email_verified=check_email_verified,
            holder=holder,
            settings=settings
        )

    return api_authenticate_user
