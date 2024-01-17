from fastapi import APIRouter
from starlette.status import HTTP_200_OK

router = APIRouter()


@router.get("/", status_code=HTTP_200_OK)
def healthcheck():
    return {"status": "ok"}
