import datetime
import orjson
from pydantic import BaseModel
from typing import Optional

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Orjson(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Event(Orjson):
    movie_timestamp: int
    movie_id: str
    user_id: int


class UserValues(Orjson):
    value: str


class FilmRate(Orjson):
    user_id: str
    movie_id: str
    rating: int


class FilmRateFilter(Orjson):
    user_id: str
    movie_id: str


class FilmInfo(Orjson):
    movie_id: str
    likes: int
    dislikes: int
    rating: float


class FilmReview(Orjson):
    movie_id: str
    user_id: str
    text: str
    timestamp: datetime.datetime


class FilmReviewAdd(Orjson):
    movie_id: str
    user_id: str
    text: str


class FilmReviewInfo(FilmReview):
    rating: Optional[int]
