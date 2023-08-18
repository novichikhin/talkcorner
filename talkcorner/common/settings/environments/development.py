from pydantic_settings import SettingsConfigDict

from talkcorner.common.settings.environments.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env.example",
        validate_assignment=True
    )
