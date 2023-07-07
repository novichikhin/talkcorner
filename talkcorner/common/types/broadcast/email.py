from pydantic import BaseModel, EmailStr


class EmailBroadcast(BaseModel):
    to_address: EmailStr
    subject: str
    html: str
