from typing import List, Optional
from uuid import UUID

from models.mixins import BaseOrjsonModelMixin
from pydantic import BaseModel


class GenreListSchema(BaseModel):
    uuid: UUID
    name: str


class GenreSchema(GenreListSchema):
    description: Optional[str] = None


class GenreList(BaseOrjsonModelMixin):
    name: str


class Genre(BaseOrjsonModelMixin):
    """Жанр кинопроизведения."""
    name: str
    description: Optional[str] = None
    film_ids: List[UUID] = []
    rating: float = 0.0
