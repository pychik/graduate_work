from http import HTTPStatus
from typing import List
from uuid import UUID

from core.errors import ApiErrors
from fastapi import APIRouter, Depends, HTTPException
from helpers import get_params
from models.person import PersonListSchema, PersonSchema
from services.persons import PersonService, get_person_service


router = APIRouter()


@router.get('/{person_id}/',
            response_model=PersonSchema,
            summary='Страница персоны',
            description='Детальная информация о персоне',
            response_description='Данные персоны с указанием ролей и фильмов',
            tags=['Персоны'])
async def person_detail(
        person_id: UUID,
        service: PersonService = Depends(get_person_service)
) -> PersonSchema:
    person = await service.get(record_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ApiErrors.person_not_found)
    return PersonSchema(**person.dict())


@router.get('/',
            response_model=List[PersonListSchema],
            summary='Список персон',
            description='Список персон с возможностью сортировки и поиска',
            response_description='Имя персоны',
            tags=['Персоны', 'Полнотекстовый поиск'])
async def person_list(
        service: PersonService = Depends(get_person_service),
        params=Depends(get_params)
) -> List[PersonListSchema]:
    params = {
        'from': params.page_number,
        'size': params.page_size,
        'sort': params.sort,
        'query': params.query
    }
    persons = await service.get(params=params)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ApiErrors.persons_not_found)
    return persons
