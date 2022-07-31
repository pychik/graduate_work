import json
import os
from typing import List

from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from loguru import logger
from utils import backoff


load_dotenv()

elastic_port = int(os.getenv('ETL_PORT'))
elastic_host = os.getenv('ETL_HOST')


class EtlConnect:

    def __init__(self, dsl):
        self.dsl = dsl
        self.es = Elasticsearch(self.dsl)

    def _check_index_exists(self, index_name: str) -> bool:
        indexes = self.es.indices.get_alias().keys()
        if index_name in indexes:
            return True
        return False

    @backoff()
    def create_index(self, index_name: str, data: List[dict]) -> None:
        if self._check_index_exists(index_name):
            logger.info(f'Index {index_name} already exists!')
        else:
            data = json.loads(data)
            self.es.indices.create(index=index_name,
                                   settings=data['settings'],
                                   mappings=data['mappings'])
            logger.info(f'Index {index_name} successfully created')

    @backoff()
    def bulk_insert(self, data: List[dict]) -> None:
        result, _ = helpers.bulk(self.es, data)
        logger.info(f'{result} rows successfully added to Elastic')
