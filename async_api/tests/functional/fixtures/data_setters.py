import pytest
from tests.functional.settings import TestSetting


@pytest.fixture(scope='class')
def genres_es_index(settings: TestSetting):
    return settings.es_genre_index


@pytest.fixture(scope='class')
def genres_es_test_data(settings: TestSetting):
    return settings.get_genres_data()


@pytest.fixture(scope='class')
async def movies_es_index(settings: TestSetting):
    return settings.es_film_index


@pytest.fixture(scope='class')
async def movies_es_test_data(settings: TestSetting):
    return settings.get_movies_data()


@pytest.fixture(scope='class')
async def persons_es_index(settings: TestSetting):
    return settings.es_person_index


@pytest.fixture(scope='class')
async def persons_es_test_data(settings: TestSetting):
    return settings.get_persons_data()
