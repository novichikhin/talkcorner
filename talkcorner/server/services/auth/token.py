import datetime as dt
from typing import Any

from jose import jwt
from jose.constants import ALGORITHMS


def create_access_token(
    payload: dict[str, Any],
    secret_key: str,
    expire_minutes: int
) -> str:
    return jwt.encode(
        claims={
            "exp": dt.datetime.utcnow() + dt.timedelta(minutes=expire_minutes),
            **payload
        },
        key=secret_key,
        algorithm=ALGORITHMS.HS256
    )
