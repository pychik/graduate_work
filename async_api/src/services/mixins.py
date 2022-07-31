import logging
from abc import abstractmethod
from collections import defaultdict
from http import HTTPStatus
from typing import ByteString, Dict, List, Optional, Union
from uuid import UUID

import orjson
from aioredis import Redis
from core.config import DEFAULT_CACHE_TIMEOUT, PROJECT_NAME
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import HTTPException
from models.film import Film
from models.genre import Genre
from models.person import Person
from pydantic import parse_obj_as
from utils import backoff


MODEL_TYPES = Union[Film, Person, Genre]

logger = logging.getLogger(PROJECT_NAME)


class SortingMixin:
    allowed_sort_fields = []
    sort_fields = []

    def get_sorting(self, sort, is_composite):
        if not sort:
            return self.sort_fields

        sort_cleared = sort.strip('-')
        if sort_cleared not in self.allowed_sort_fields:
            return []

        field = sort_cleared if not is_composite else f'{sort_cleared}.keyword'
        order = 'desc' if sort.startswith('-') else 'asc'

        return [{
            field: {'order': order}
        }]


class BaseServiceMixin(SortingMixin):
    CACHE_EXPIRE_IN_SECONDS = 60 * 5
    separator = '::'

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.cache = CacheStorage(redis)
        self.database = DataBaseStorage(
            elastic,
            cache=self.cache,
            elastic_index=self.elastic_index,
            filter_fields=self.filter_fields,
            allowed_sort_fields=self.allowed_sort_fields
        )

    @property
    @abstractmethod
    def elastic_index(self) -> str:
        pass

    @property
    @abstractmethod
    def filter_fields(self) -> List:
        pass

    @staticmethod
    @abstractmethod
    def model(*args, **kwargs) -> MODEL_TYPES:
        pass

    async def get(
            self,
            record_id: UUID = None,
            params: dict = None
    ) -> Union[Optional[MODEL_TYPES], List[Optional[MODEL_TYPES]]]:
        # В зависимости от запроса, возвращает детальную информацию об объекте либо список объектов
        detail = True if record_id else False
        key = await self._generate_cache_key(record_id=record_id, params=params)
        data = await self.cache.get(key)
        if not data:
            if record_id:
                data = await self.database.get(record_id)
            else:
                data = await self.database.search(index=self.elastic_index, params=params)
            if not data:
                return None
        data = await self._generate_answer(data, detail)
        await self.cache.set(key, data, expire=self.CACHE_EXPIRE_IN_SECONDS)
        return data

    async def _generate_cache_key(self, record_id: UUID = None, params: dict = None) -> str:
        if record_id:
            return f'{self.elastic_index}-record-{record_id}'

        params = [item for pair in params.items() for item in pair]

        params_string = self.separator.join(str(item) for item in params)
        return f'{self.elastic_index}-list-{params_string}'

    async def _generate_answer(self,
                               data: Union[ByteString, dict, List[dict]],
                               detail: bool = False):
        if detail:
            if isinstance(data, ByteString):
                return self.model.parse_raw(data)
            return self.model(**data)
        else:
            if isinstance(data, ByteString):
                return [self.model.parse_raw(item) for item in orjson.loads(data)]
            return parse_obj_as(List[self.model], data)


class CacheStorage:
    """
    Базовый класс для работы с Redis.
    :param client - авторизованный клиент Redis
    """
    def __init__(self, client):
        self.client = client
        self.default_cache_timeout = DEFAULT_CACHE_TIMEOUT

    @backoff()
    async def get(self, key: str):
        return await self.client.get(key)

    @backoff()
    async def set(self,
                  key: str,
                  data: Union[List[MODEL_TYPES], Optional[MODEL_TYPES], ByteString],
                  expire: int = None):
        # Если timeout не задан, используем по умолчанию.
        if not expire:
            expire = self.default_cache_timeout

        if not isinstance(data, ByteString):
            if isinstance(data, list):
                data = orjson.dumps([item.json() for item in data])
            else:
                data = data.json()

        await self.client.set(key, data, expire=expire)


class DataBaseStorage(SortingMixin):
    """
    Базовый класс для работы с Elasticsearch.
    :param database_client - авторизованный клиент базы данных
    :param cache - Redis Кэш
    :param filter_fields - Поля по которым применим фильтр
    :param elastic_index - Индекс Elastic
    :param allowed_sort_fields - Поля по которым применима сортировка
    """
    def __init__(self, database_client: AsyncElasticsearch, cache: CacheStorage, **kwargs):
        self.client = database_client
        self.cache = cache
        self.filter_fields = kwargs.get('filter_fields' or None)
        self.elastic_index = kwargs.get('elastic_index' or None)
        self.allowed_sort_fields = kwargs.get('allowed_sort_fields' or None)

    @backoff()
    async def get(self, record_id: UUID) -> Union[dict, None]:
        try:
            doc = await self.client.get(self.elastic_index, record_id)
        except NotFoundError:
            return None
        return doc['_source']

    @backoff()
    async def search(self, index: str, params: dict) -> List[dict]:
        is_composite_sort = await self._check_composite_sort_field(params['sort'])
        body = self._get_search_body(params, is_composite_sort)
        data = await self.client.search(index=index, body=body)
        return [x['_source'] for x in data['hits']['hits']]

    @backoff()
    async def _get_sortable_indexes(self) -> Dict[str, bool]:
        """Получение схемы полей для сортировки."""
        index = f'{self.elastic_index}-sortable_fields'
        schemas = await self.cache.get(index)
        if not schemas:
            schemas = defaultdict()
            try:
                fields_info = await self.client.field_caps(
                    fields=','.join(self.allowed_sort_fields),
                    index=self.elastic_index
                )
            except NotFoundError:
                logger.error('Index not FOUND!')
                msg = 'Request cannot be processed: Index not FOUND!'
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg)

            for field in self.allowed_sort_fields:
                schemas[field] = 'text' in fields_info['fields'][field].keys()

            await self.cache.set(index, orjson.dumps(schemas), expire=DEFAULT_CACHE_TIMEOUT)
            return schemas

        return orjson.loads(schemas)

    async def _check_composite_sort_field(self, field: Optional[str]) -> bool:
        """
        Проверка является ли переданное поле составным.
        :param field - название поля для сортировки
        """
        if not field:
            return False
        cleared_index = field.strip('-')
        index_schemas = await self._get_sortable_indexes()
        return index_schemas.get(cleared_index, False)

    def _get_search_body(self, params, is_composite_sort) -> dict:
        """
        Получение body для поиска данных в ElasticSearch
        :param params - параметры из запроса для формирования body
        :param is_composite_sort - флаг является ли поле сортировки составным
        """
        query_param = params.get('query')

        body = defaultdict()
        body['size'] = params['size']
        body['from'] = (params['from'] - 1) * params['size']
        body['query'] = defaultdict()
        body['sort'] = self.get_sorting(params['sort'], is_composite_sort)

        if query_param:
            body['query']['query_string'] = {
                'query': query_param,
                'fields': self.filter_fields
            }
        else:
            body['query']['match_all'] = defaultdict()

        return body
