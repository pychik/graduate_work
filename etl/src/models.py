from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.schema import List, Optional


class Movie(BaseModel):
    uuid: UUID
    imdb_rating: float = Field(alias='rating', default=0.0)
    genre: Optional[List]
    title: str
    description: Optional[str]
    director: Optional[List] = Field(alias='director', default=[])
    actors_names: Optional[List]
    actors: Optional[List]
    writers_names: Optional[List]
    writers: Optional[List]
