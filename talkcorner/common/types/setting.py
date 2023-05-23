from pydantic import BaseSettings, Field


class Setting(BaseSettings):
    API_V1_STR: str = Field(default="/api/v1")

    SERVER_HOST: str = Field(default="127.0.0.1")
    SERVER_PORT: int = Field(default=8080)

    DATABASE_URI: str = Field(default=...)

    NATS_URL: str = Field(default=...)
    NATS_STREAM_NAME: str = Field(default=...)

    AUTHORIZE_SECRET_KEY: str = Field(default=...)
    AUTHORIZE_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=...)
    AUTHORIZE_REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=...)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
