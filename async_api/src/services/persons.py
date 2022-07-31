from functools import lru_cache

from db.base import AsyncCacheService, AsyncSearchService
from db.cache import get_redis
from db.search_service import get_elastic
from fastapi import Depends
from models.person import Person
from services.mixins import BaseServiceMixin


class PersonService(BaseServiceMixin):
    CACHE_EXPIRE_IN_SECONDS = 60 * 10
    elastic_index = 'persons'
    model = Person
    filter_fields = ['full_name']
    allowed_sort_fields = ['full_name']
    sort_fields = [
        {'full_name.keyword': {'order': 'asc'}}
    ]


@lru_cache()
def get_person_service(
        cache: AsyncCacheService = Depends(get_redis),
        search_service: AsyncSearchService = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, search_service)
