import os

from elasticsearch import Elasticsearch
from utils import backoff


ELASTIC_PORT = int(os.getenv('ETL_PORT'))
ELASTIC_HOST = os.getenv('ETL_HOST')


@backoff()
def check():
    es = Elasticsearch(
        hosts=f'http://{ELASTIC_HOST}:{ELASTIC_PORT}',
        verify_certs=True
    )
    if not es.ping():
        raise Exception('Elastic is not ready')


if __name__ == '__main__':
    check()
