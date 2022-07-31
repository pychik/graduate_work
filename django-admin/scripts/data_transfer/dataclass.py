import datetime
import uuid
from dataclasses import dataclass


class DataClassGetter:

    def __init__(self, table):
        self.table = table

    def get_dataclass(self):
        if self.table == 'film_work':
            return FilmWork
        elif self.table == 'genre':
            return Genre
        elif self.table == 'person':
            return Person
        elif self.table == 'genre_film_work':
            return GenreFilmWork
        elif self.table == 'person_film_work':
            return PersonFilmWork
        else:
            raise Exception("Not yet implemented")


@dataclass
class FilmWork:
    title: str
    description: str
    creation_date: datetime.datetime
    rating: float
    file_path: str
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID


@dataclass
class GenreFilmWork:
    created_at: datetime.datetime
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    id: uuid.UUID


@dataclass
class Person:
    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID


@dataclass
class PersonFilmWork:
    role: str
    created_at: datetime.datetime
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    id: uuid.UUID
