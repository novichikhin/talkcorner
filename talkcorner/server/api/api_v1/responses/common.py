from pydantic import BaseModel


class Error(BaseModel):
    status: str = "fail"


class Validation(Error):
    detail: str


class SomethingWentWrong(Error):
    detail: str = "Something went wrong"
