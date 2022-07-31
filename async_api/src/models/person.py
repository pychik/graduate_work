from enum import Enum
from typing import List
from uuid import UUID

from models.mixins import BaseOrjsonModelMixin
from pydantic import BaseModel


class RoleEnum(str, Enum):
    """Роль участника."""
    ACTOR = 'actor'
    SOUND_DIRECTOR = 'sound_director'
    DIRECTOR = 'director'
    MUSIC_EDITOR = 'music_director'
    WRITER = 'writer'


class PersonListSchema(BaseModel):
    uuid: UUID
    full_name: str


class PersonSchema(PersonListSchema):
    role: List[RoleEnum] = []
    film_ids: List[UUID] = []


class Person(BaseOrjsonModelMixin):
    """Участник."""
    full_name: str
    role: List[RoleEnum] = []
    film_ids: List[UUID] = []
