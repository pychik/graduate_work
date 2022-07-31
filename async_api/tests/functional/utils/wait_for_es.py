from elasticsearch import Elasticsearch
from tests.functional.settings import settings
from utils import backoff


@backoff()
def check():
    es = Elasticsearch(
        hosts=[settings.es_host],
        port=settings.es_port,
        verify_certs=True
    )
    es.ping()


if __name__ == '__main__':
    check()
