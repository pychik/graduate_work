from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModelMixin(BaseModel):
    uuid: UUID

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ParamsMixin(BaseModel):
    page_number: int = Field(default=1)
    page_size: int = Field(default=50)
    sort: Optional[str] = None
    query: Optional[str] = None
