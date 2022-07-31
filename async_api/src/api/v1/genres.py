from http import HTTPStatus
from typing import List
from uuid import UUID

from core.errors import ApiErrors
from fastapi import APIRouter, Depends, HTTPException
from helpers import get_params
from models.genre import GenreListSchema, GenreSchema
from services.genres import GenreService, get_genre_service


router = APIRouter()


@router.get('/{genre_id}/',
            response_model=GenreSchema,
            summary='Страница жанра',
            description='Детальная информация о жанре',
            response_description='Название и описание жанра',
            tags=['Жанры'])
async def genre_detail(
        genre_id: UUID,
        service: GenreService = Depends(get_genre_service)
) -> GenreSchema:
    genre = await service.get(record_id=genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ApiErrors.genre_not_found)
    return GenreSchema(**genre.dict())


@router.get('/',
            response_model=List[GenreListSchema],
            summary='Список жанров',
            description='Список жанров с возможностью сортировки и поиска',
            response_description='Название жанра',
            tags=['Жанры', 'Полнотекстовый поиск'])
async def genre_list(
        service: GenreService = Depends(get_genre_service),
        params=Depends(get_params)
) -> List[GenreListSchema]:
    params = {
        'from': params.page_number,
        'size': params.page_size,
        'sort': params.sort,
        'query': params.query,
    }
    genres = await service.get(params=params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ApiErrors.genres_not_found)
    return genres
