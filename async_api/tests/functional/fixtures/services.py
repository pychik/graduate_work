import pytest
from elasticsearch import Elasticsearch
from redis import Redis


@pytest.fixture(scope='session')
async def es_client(settings):
    client = Elasticsearch(hosts=settings.es_url)
    yield client
    client.close()


@pytest.fixture(scope='session')
async def redis_client(settings):
    client = Redis(host=settings.redis_host, port=settings.redis_port)
    yield client
    client.flushall()
    client.close()
