from functools import lru_cache

from db.base import AsyncCacheService, AsyncSearchService
from db.cache import get_redis
from db.search_service import get_elastic
from fastapi import Depends
from models.film import Film
from services.mixins import BaseServiceMixin


class FilmService(BaseServiceMixin):
    CACHE_EXPIRE_IN_SECONDS = 60 * 5
    elastic_index = 'movies'
    model = Film
    filter_fields = ['title']
    allowed_sort_fields = ['imdb_rating', 'title']
    sort_fields = [
        {'imdb_rating': {'order': 'desc'}}
    ]


@lru_cache()
def get_film_service(
        cache: AsyncCacheService = Depends(get_redis),
        search_service: AsyncSearchService = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache, search_service)
