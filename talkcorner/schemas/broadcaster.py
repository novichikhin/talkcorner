from pydantic import EmailStr

from talkcorner.schemas.base import BaseSchema


class EmailBroadcast(BaseSchema):
    to_address: EmailStr
    subject: str
    html: str
