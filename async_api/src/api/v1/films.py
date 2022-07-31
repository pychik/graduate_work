from http import HTTPStatus
from typing import List
from uuid import UUID

from core.errors import ApiErrors
from fastapi import APIRouter, Depends, HTTPException
from helpers import get_params
from models.film import FilmBasicSchema, FilmDetailSchema
from services.films import FilmService, get_film_service


router = APIRouter()


@router.get('/search',
            response_model=List[FilmBasicSchema],
            summary='Поиск кинопроизведений',
            description='Полнотекстовый поиск по кинопроизведениям',
            response_description='Название и рейтинг фильма',
            tags=['Полнотекстовый поиск'])
async def film_search(
        params=Depends(get_params),
        film_service: FilmService = Depends(get_film_service)
) -> List[FilmBasicSchema]:
    params = {
        'from': params.page_number,
        'size': params.page_size,
        'sort': params.sort,
        'query': params.query
    }

    if films := await film_service.get(params=params):
        return [FilmBasicSchema(uuid=film.uuid,
                                title=film.title,
                                imdb_rating=film.imdb_rating) for film in films]

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ApiErrors.films_not_found)


@router.get('/{film_id}',
            response_model=FilmDetailSchema,
            summary='Страница кинопроизведения',
            description='Детальная информация по кинопроизведению',
            response_description='Данные фильма',
            tags=['Кинопроизведения'])
async def film_details(film_id: UUID,
                       film_service: FilmService = Depends(get_film_service)) -> FilmDetailSchema:
    film = await film_service.get(record_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ApiErrors.film_not_found)

    return FilmDetailSchema(uuid=film.uuid,
                            title=film.title,
                            imdb_rating=film.imdb_rating,
                            description=film.description,
                            genre=film.genre,
                            actors=film.actors,
                            writers=film.writers,
                            directors=film.directors)


@router.get('/',
            # response_model=List,
            summary='Список кинопроизведений',
            description='Список кинопроизведений с возможностью сортировки',
            response_description='Название и рейтинг фильма',
            tags=['Кинопроизведения'])
async def film_main_page(
        params=Depends(get_params),
        film_service: FilmService = Depends(get_film_service)
):
    params = {
        'from': params.page_number,
        'size': params.page_size,
        'sort': params.sort,
    }

    if films := await film_service.get(params=params):
        return [FilmBasicSchema(uuid=film.uuid,
                                title=film.title,
                                imdb_rating=film.imdb_rating) for film in films]

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ApiErrors.films_not_found)
