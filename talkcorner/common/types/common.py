from typing import Any

from pydantic import BaseModel, root_validator


class Update(BaseModel):

    @root_validator
    def root_validator_update(cls, values: dict[str, Any]) -> dict[str, Any]:
        if all(not value for value in values.values()):
            raise ValueError("at least one value must be filled in")
        return values
