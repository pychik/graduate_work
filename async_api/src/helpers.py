import aiohttp
from fastapi import Query
from models.mixins import ParamsMixin


def get_params(
    page_number: int = Query(1, ge=1, title='Номер страницы', alias='page[number]'),
    page_size: int = Query(
        10, ge=1, le=50, title='Количество записей', alias='page[size]'
    ),
    sort: str = Query(None, title='Сортировка', alias='sort'),
    query: str = Query(None, title='Поиск', alias='query')
):
    return ParamsMixin(
        page_size=page_size,
        page_number=page_number,
        sort=sort,
        query=query
    )


async def check_authorization(url, headers):

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            return await response.json()
