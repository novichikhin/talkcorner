from typing import Optional

from pydantic import BaseSettings, Field
from pydantic.env_settings import env_file_sentinel, DotenvType


class Setting(BaseSettings):

    def __init__(
            self,
            _env_file: Optional[DotenvType] = env_file_sentinel,
            **kwargs
    ):
        super().__init__(_env_file=_env_file, **kwargs)

    api_v1_str: str = Field(default="/api/v1")

    server_host: str = Field(default="127.0.0.1")
    server_port: int = Field(default=8080)

    database_uri: str = Field(default=...)

    nats_url: str = Field(default=...)
    nats_stream_name: str = Field(default=...)

    authorize_access_token_secret_key: str = Field(default=...)
    authorize_refresh_token_secret_key: str = Field(default=...)
    authorize_access_token_expire_minutes: int = Field(default=...)
    authorize_refresh_token_expire_minutes: int = Field(default=...)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
