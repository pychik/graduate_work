from functools import lru_cache

from db.base import AsyncCacheService, AsyncSearchService
from db.cache import get_redis
from db.search_service import get_elastic
from fastapi import Depends
from models.genre import Genre
from services.mixins import BaseServiceMixin


class GenreService(BaseServiceMixin):
    CACHE_EXPIRE_IN_SECONDS = 60 * 60
    elastic_index = 'genres'
    model = Genre
    filter_fields = ['name']
    allowed_sort_fields = ['name']
    sort_fields = [
        {'name.keyword': {'order': 'asc'}}
    ]


@lru_cache()
def get_genre_service(
        cache: AsyncCacheService = Depends(get_redis),
        search_service: AsyncSearchService = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, search_service)
