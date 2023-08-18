from typing import Callable, Awaitable

from fastapi import Header, Depends

from talkcorner.common.settings.app import AppSettings
from talkcorner.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from talkcorner.server.api.api_v1.dependencies.setting import SettingsMarker
from talkcorner.server.database.holder import DatabaseHolder
from talkcorner.server.schemas.auth import RefreshToken
from talkcorner.server.schemas.user import User
from talkcorner.server.services.auth.main import verify_refresh_token, get_user


async def api_verify_refresh_token(
    authorization: str = Header(alias="Authorization"),
    settings: AppSettings = Depends(SettingsMarker)
) -> RefreshToken:
    return await verify_refresh_token(
        authorization=authorization,
        settings=settings
    )


def api_get_user(
    check_email_verified: bool = True
) -> Callable[[str, DatabaseHolder, AppSettings], Awaitable[User]]:

    async def api_get_user(
            authorization: str = Header(alias="Authorization"),
            holder: DatabaseHolder = Depends(DatabaseHolderMarker),
            settings: AppSettings = Depends(SettingsMarker)
    ) -> User:
        return await get_user(
            authorization=authorization,
            check_email_verified=check_email_verified,
            holder=holder,
            settings=settings
        )

    return api_get_user
