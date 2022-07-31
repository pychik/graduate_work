from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID

from models.mixins import BaseOrjsonModelMixin


LIST_DICT_TYPE = Union[List[Dict[str, Union[str, UUID]]], None]


class FilmTypeEnum(str, Enum):
    """Тип кинопроизведения."""
    MOVIE = 'movie'
    TV_SHOW = 'tv_show'


class FilmBasicSchema(BaseOrjsonModelMixin):
    title: str
    imdb_rating: float = 0.0


class FilmDetailSchema(FilmBasicSchema):
    description: Optional[str] = ''
    genre: List[str] = []
    actors: LIST_DICT_TYPE = []
    writers: LIST_DICT_TYPE = []
    directors: LIST_DICT_TYPE = []


class Film(BaseOrjsonModelMixin):
    """Кинопроизведение."""
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    file_link: Optional[str] = None
    age_limit: int = 0
    imdb_rating: float = 0
    type: FilmTypeEnum = FilmTypeEnum.MOVIE
    genre: List[str] = []
    actors: LIST_DICT_TYPE = []
    writers: LIST_DICT_TYPE = []
    directors: LIST_DICT_TYPE = []
