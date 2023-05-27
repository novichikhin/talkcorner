from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR


async def http_exception_handler(_: Request, e: HTTPException) -> JSONResponse:
    headers = getattr(e, "headers", None)
    if headers:
        return JSONResponse(
            {"status": "fail", "detail": e.detail},
            status_code=e.status_code,
            headers=headers
        )
    else:
        return JSONResponse({"status": "fail", "detail": e.detail}, status_code=e.status_code)


async def request_validation_error_handler(_: Request, e: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "fail", "detail": str(e)}
    )


async def exception_handler(_: Request, e: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "fail", "detail": "Something went wrong"}
    )
