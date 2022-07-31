import pytest
from tests.functional.utils.helpers import (
    create_index_to_es,
    load_data_to_es,
    remove_data_from_es,
    remove_data_from_redis,
)


@pytest.fixture(scope='class')
async def setup_genres(redis_client,
                       es_client,
                       genres_es_index,
                       genres_es_test_data):
    await remove_data_from_redis(redis_client, 'genres')

    await create_index_to_es(es_client, genres_es_index)
    await load_data_to_es(es_client, genres_es_index, genres_es_test_data)
    yield genres_es_test_data
    await remove_data_from_es(es_client, genres_es_index, genres_es_test_data)


@pytest.fixture(scope='class')
async def setup_movies(redis_client,
                       es_client,
                       movies_es_index,
                       movies_es_test_data):
    await remove_data_from_redis(redis_client, 'movies')

    await create_index_to_es(es_client, movies_es_index)
    await load_data_to_es(es_client, movies_es_index, movies_es_test_data)
    yield movies_es_test_data

    await remove_data_from_es(es_client, movies_es_index, movies_es_test_data)


@pytest.fixture(scope='class')
async def setup_persons(redis_client,
                        es_client,
                        persons_es_index,
                        persons_es_test_data):
    await remove_data_from_redis(redis_client, 'persons')
    await create_index_to_es(es_client, persons_es_index)
    await load_data_to_es(es_client, persons_es_index, persons_es_test_data)
    yield persons_es_test_data

    await remove_data_from_es(es_client, persons_es_index, persons_es_test_data)
