import http
import random
import string

import pytest
from functional.utils.helpers import remove_data_from_es, transform_films_search


class TestSearch:
    @pytest.mark.asyncio
    async def test_films_search(self, setup_movies, make_request):
        """Тестируем полное совпадение."""
        query = setup_movies[0]['title']
        response = await make_request(f'films/search?query={query}')
        test_data = transform_films_search(setup_movies, query)
        assert response.status == http.HTTPStatus.OK
        assert response.body == test_data
        assert len(response.body) == len(test_data)

    @pytest.mark.asyncio
    async def test_films_search_overlap(self, setup_movies, make_request):
        """Тестируем частичное совпадение."""
        query = setup_movies[0]['title'].split(' ')[0]
        response = await make_request(f'films/search?query={query}')
        test_data = transform_films_search(setup_movies, query)
        test_data = sorted(test_data, key=lambda d: d['imdb_rating'])
        assert response.status == http.HTTPStatus.OK
        assert response.body == test_data
        assert len(response.body) == len(test_data)

    @pytest.mark.asyncio
    async def test_films_search_404(self, setup_movies, make_request):
        """Тестируем поиск отсутствующего фильма."""
        query = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        response = await make_request(f'films/search?query={query}')
        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'There is no films yet'}

    @pytest.mark.asyncio
    async def test_films_search_cache(
            self,
            es_client,
            setup_movies,
            make_request,
            movies_es_index):
        """Тест кеширования."""
        query = setup_movies[0]['title'].split(' ')[0]
        response = await make_request(f'films/search?query={query}')

        assert response.status == http.HTTPStatus.OK
        await remove_data_from_es(es_client, movies_es_index, setup_movies)

        response = await make_request(f'films/search?query={query}')

        assert response.status == http.HTTPStatus.OK
