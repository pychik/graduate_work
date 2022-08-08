import datetime
from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Orjson(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmUser(Orjson):
    """Базовая модель."""
    movie_id: str
    user_id: int


class Event(FilmUser):
    movie_timestamp: int


class UserValues(Orjson):
    value: str


class FilmRate(FilmUser):
    rating: int


class FilmInfo(Orjson):
    movie_id: str
    likes: int
    dislikes: int
    rating: float


class FilmReview(FilmUser):
    text: str
    timestamp: datetime.datetime


class FilmReviewAdd(FilmUser):
    text: str


class FilmReviewInfo(FilmReview):
    rating: Optional[int]


class FilmBookmarks(FilmUser):
    """Контент добавленный в закладки пользователей."""
    created_at: datetime.datetime
