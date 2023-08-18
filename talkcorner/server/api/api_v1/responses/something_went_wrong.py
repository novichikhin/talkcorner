from talkcorner.server.api.api_v1.responses.base import BaseResponse


class SomethingWentWrong(BaseResponse):
    detail: str = "Something went wrong"
