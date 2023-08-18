from typing import Any

from pydantic import BaseModel, model_validator


class BaseSchema(BaseModel):
    pass


class BaseUpdate(BaseSchema):

    @model_validator(mode="before")
    def model_validator_update(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not len(data):
                raise ValueError("at least one value must be filled in")
        return data
