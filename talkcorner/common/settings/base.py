from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        validate_assignment=True
    )
