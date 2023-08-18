import uuid

from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    token: str
    user_id: uuid.UUID


class Authentication(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
