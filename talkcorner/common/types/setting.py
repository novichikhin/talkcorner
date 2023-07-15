from typing import Optional

from pydantic import BaseSettings, Field, EmailStr
from pydantic.env_settings import env_file_sentinel, DotenvType


class Settings(BaseSettings):

    def __init__(
            self,
            _env_file: Optional[DotenvType] = env_file_sentinel,
            **kwargs
    ):
        super().__init__(_env_file=_env_file, **kwargs)

    api_v1_str: str = Field(default="/api/v1")

    server_host: str = Field(default="127.0.0.1")
    server_port: int = Field(default=8080)

    pg_driver: str = Field(default=...)
    pg_host: str = Field(default=...)
    pg_port: int = Field(default=...)
    pg_user: str = Field(default=...)
    pg_password: str = Field(default=...)
    pg_db: str = Field(default=...)

    nats_host: str = Field(default=...)
    nats_client_port: int = Field(default=...)
    nats_user: str = Field(default=...)
    nats_password: str = Field(default=...)
    nats_stream_name: str = Field(default=...)

    authorize_access_token_secret_key: str = Field(default=...)
    authorize_refresh_token_secret_key: str = Field(default=...)
    authorize_access_token_expire_minutes: int = Field(default=...)
    authorize_refresh_token_expire_minutes: int = Field(default=...)

    email_host: str = Field(default=...)
    email_port: int = Field(default=...)
    email_from_address: EmailStr = Field(default=...)
    email_password: str = Field(default=...)
    email_verify_url: str = Field(default=...)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
