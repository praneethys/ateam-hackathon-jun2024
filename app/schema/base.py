from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PydanticBaseModel(BaseModel):
    pass


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
