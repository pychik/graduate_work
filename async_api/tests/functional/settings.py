import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, BaseSettings, Field, PrivateAttr


@dataclass
class HTTPResponse:
    body: Dict
    headers: Dict
    status: int


class TestDataLoader(BaseModel):
    _movies: Optional[List[Dict]] = PrivateAttr(default_factory=list)
    _genres: Optional[List[Dict]] = PrivateAttr(default_factory=list)
    _persons: Optional[List[Dict]] = PrivateAttr(default_factory=list)
    _current_directory: Path = PrivateAttr(default=Path(__file__).parent.resolve())

    def __load_test_data(self, field, file_name):
        value = getattr(self, field)
        if value:
            return value

        with open(f'{self._current_directory}/testdata/{file_name}', 'r') as file:
            value = json.load(file)
            setattr(self, field, value)

        return value

    def get_movies_data(self):
        return self.__load_test_data('_movies', 'movies.json')

    def get_genres_data(self):
        return self.__load_test_data('_genres', 'genres.json')

    def get_persons_data(self):
        return self.__load_test_data('_persons', 'persons.json')


class TestSetting(TestDataLoader, BaseSettings):
    api_host: str = Field('http://0.0.0.0', env='API_HOST')
    api_port: int = Field(8000, env='API_PORT')
    api_version: str = Field('v1', env='API_VERSION')

    es_host: str = Field('http://127.0.0.1', env='ELASTIC_HOST')
    es_port: int = Field(6379, env='ELASTIC_PORT')
    es_film_index: str = Field('movies', env='ELASTIC_FILM_INDEX')
    es_genre_index: str = Field('genres', env='ELASTIC_GENRE_INDEX')
    es_person_index: str = Field('persons', env='ELASTIC_PERSON_INDEX')

    redis_host: str = Field('http://127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(9200, env='REDIS_PORT')

    @property
    def __base_api_url(self) -> str:
        return f'http://{self.api_host}:{self.api_port}/api/{self.api_version}'

    @property
    def es_url(self):
        return f'{self.es_host}:{self.es_port}'

    def get_api_url(self, part: str):
        return f'{self.__base_api_url}/{part}'


settings = TestSetting()
