from pydantic import BaseSettings


class Setting(BaseSettings):
    API_V1_STR: str = "/api/v1"

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8080

    DATABASE_URI: str

    NATS_URL: str
    NATS_STREAM_NAME: str

    AUTHORIZE_SECRET_KEY: str
    AUTHORIZE_ACCESS_TOKEN_EXPIRE_MINUTES: int
    AUTHORIZE_REFRESH_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
