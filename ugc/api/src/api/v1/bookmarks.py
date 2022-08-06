from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Request
from models.models import FilmBookmarks, FilmUser
from service.bookmarks import BookmarksService, get_service


router = APIRouter()


@router.post(
    '/',
    response_model=FilmBookmarks,
    response_model_exclude_unset=True,
    tags=['Ugc film bookmarks'],
    summary='Создание новых закладок.',
    description='Добавление контента в закладки.',
    status_code=HTTPStatus.CREATED
)
@router.delete(
    '/',
    response_model_exclude_unset=True,
    tags=['Ugc film bookmarks'],
    summary='Удаление существующих закладок.',
    description='Будет произведено удаление существующей закладки.',
    status_code=HTTPStatus.NO_CONTENT
)
async def bookmarks(
    request: Request,
    data: FilmUser,
    service: BookmarksService = Depends(get_service)
) -> FilmBookmarks:
    if request.method == 'POST':
        result = await service.save(user_id=data.user_id, movie_id=data.movie_id)
        return result

    # Delete instance.
    obj = await service.delete(user_id=data.user_id, movie_id=data.movie_id)
    response = dict(status='Success!', object=obj)
    return response


@router.get(
    '/{user_id}',
    response_model=List[FilmBookmarks],
    response_model_exclude_unset=True,
    tags=['Ugc film bookmarks'],
    summary='Список закладок пользователя.',
    description='Будет возвращен список закладок пользователя.',
    status_code=HTTPStatus.OK
)
async def list_bookmark(user_id: int, service: BookmarksService = Depends(get_service)):
    data = await service.get_list(user_id=user_id)
    return data
