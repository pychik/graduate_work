import datetime
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from config import settings
from models.models import (FilmInfo,
                           FilmRate,
                           FilmRateFilter,
                           FilmReview,
                           FilmReviewAdd,
                           FilmReviewInfo)

from service.rating import RatingService, get_rating_service

router = APIRouter()


@router.get("/{film_id}/likes",
            response_model=FilmInfo,
            response_model_exclude_unset=True, tags=['Ugc films rating'],
            summary='Пользовательский рейтинг фильмов',
            description='показывает оценки пользователей',
            status_code=200)
async def film_likes(film_id: str, film_service: RatingService = Depends(get_rating_service)) -> FilmInfo:
    film_info = await film_service.get_film_info(film_id)
    if not film_info:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.UgcErrors.likes_not_found)
    return film_info


@router.post("/rate",
             response_model=FilmRate,
             response_model_exclude_unset=True,
             tags=['Ugc films rating'],
             summary='Установка пользовательской оценки фильмам',
             description='Сервис оценок фильмов',
             status_code=200)
async def update_rate(film_rate: FilmRate, rating_service: RatingService = Depends(get_rating_service)) -> FilmRate:
    result = await rating_service.update_film_rate(
        film_id=film_rate.movie_id, user_id=film_rate.user_id, rating=film_rate.rating
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.UgcErrors.likes_not_found)
    return result


@router.delete("/rate",
               tags=['Ugc films rating'],
               summary='Удаление пользовательской оценки фильма',
               description='Сервис удаления пользовательского оценки фильма',
               status_code=204)
async def remove_rate(film_rate: FilmRateFilter, rating_service: RatingService = Depends(get_rating_service)):
    result = await rating_service.remove_film_rate(
        film_id=film_rate.movie_id, user_id=film_rate.user_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.UgcErrors.likes_not_found)


@router.post("/review/info",
             response_model=FilmReviewInfo,
             response_model_exclude_unset=True,
             tags=['Ugc film reviews'],
             summary='Предоставление пользовательских рецензий к фильмам',
             description='Сервис рецензий',
             status_code=200)
async def get_review_info(film_review: FilmRateFilter,
                          rating_service: RatingService = Depends(get_rating_service)) -> FilmReview:
    result = await rating_service.get_film_review_info(film_id=film_review.movie_id, user_id=film_review.user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=settings.UgcErrors.reviews_not_found)
    return result


@router.post("/review",
             response_model=FilmReview,
             response_model_exclude_unset=True,
             tags=['Ugc film reviews'],
             summary='Фиксация пользовательских рецензий фильмам',
             description='Сервис получения рецензий',
             status_code=200)
async def update_review(film_review: FilmReviewAdd,
                        rating_service: RatingService = Depends(get_rating_service)) -> FilmReview:
    result = await rating_service.update_film_review(
                                                    film_id=film_review.movie_id,
                                                    user_id=film_review.user_id,
                                                    text=film_review.text,
                                                    timestamp=datetime.datetime.now(),
                                                    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=settings.UgcErrors.reviews_not_found)
    return result


@router.delete("/review",
               tags=['Ugc film reviews'],
               summary='Удаление пользовательских рецензий фильмам',
               description='Сервис удаления пользовательских рецензий',
               status_code=204)
async def delete_review(film_review: FilmRateFilter, rating_service: RatingService = Depends(get_rating_service)):
    result = await rating_service.remove_film_review(
        film_id=film_review.movie_id, user_id=film_review.user_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
