from pydantic import BaseModel


class Authorization(BaseModel):
    access_token: str
    token_type: str
