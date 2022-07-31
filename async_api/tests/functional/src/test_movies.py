import http
import uuid

import pytest
from tests.functional.utils.helpers import remove_data_from_es, transform_movies_data


class TestMovies:

    @pytest.mark.asyncio
    async def test_movies_all(self, make_request, setup_movies):
        """Тест запроса всех фильмов"""

        test_data = transform_movies_data(setup_movies)

        response = await make_request('films/')

        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == len(test_data)
        assert response.body == test_data

    @pytest.mark.asyncio
    async def test_movies_detail(self, make_request, setup_movies):
        """Тест запроса конкретного фильма"""

        movie_uuid = setup_movies[0]['uuid']

        response = await make_request(f'films/{movie_uuid}')

        assert response.status == http.HTTPStatus.OK
        assert response.body == setup_movies[0]

    @pytest.mark.asyncio
    async def test_movies_detail_404(self, make_request, setup_movies):
        """Тест запроса конкретного фильма, которого нет"""

        movie_uuid = uuid.uuid4()

        response = await make_request(f'films/{movie_uuid}')

        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'Film not found'}

    @pytest.mark.asyncio
    async def test_movies_list_sorted(self, make_request, setup_movies):
        """Тест запроса фильмов с сортировкой и размером страницы"""

        sorting = 'title'
        page_size = 1

        response = await make_request(f'films/?sort={sorting}&page[size]={page_size}')

        test_data = transform_movies_data(setup_movies)
        sorted_test_data = sorted(test_data, key=lambda x: x[sorting])

        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == page_size
        assert response.body == sorted_test_data[:page_size]

    @pytest.mark.asyncio
    async def test_movies_pagination(self, make_request, setup_movies):
        """Тест пагинации при запросе фильмов"""

        page_size = 1
        page_num = 2

        test_data = transform_movies_data(setup_movies)

        response = await make_request(f'films/?page[size]={page_size}&page[number]={page_num}')

        assert response.status == http.HTTPStatus.OK
        assert response.body == test_data[page_num - 1: page_num * page_size]

    @pytest.mark.asyncio
    async def test_movies_cache(self, make_request, setup_movies, es_client, movies_es_index):
        """Тест кеширования при запросе фильмов"""

        response = await make_request('films/')

        assert response.status == http.HTTPStatus.OK
        await remove_data_from_es(es_client, movies_es_index, setup_movies)

        second_response = await make_request('films/')

        assert second_response.status == http.HTTPStatus.OK
