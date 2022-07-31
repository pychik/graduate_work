import orjson
from pydantic import BaseModel

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Event(BaseModel):
    movie_timestamp: int
    movie_id: str
    user_id: int

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserValues(BaseModel):
    value: str
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
