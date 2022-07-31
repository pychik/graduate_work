import http
import uuid

import pytest
from functional.utils.helpers import remove_data_from_es, transform_genre_data


class TestGenres:
    @pytest.mark.asyncio
    async def test_genres_index(self, setup_genres, make_request):
        """Вывод всех жанров."""
        expected = transform_genre_data(setup_genres)

        response = await make_request('genres/')
        assert response.status == http.HTTPStatus.OK
        assert response.body == expected
        assert len(response.body) == len(expected)

    @pytest.mark.asyncio
    async def test_genres_detail(self, setup_genres, make_request):
        """Детальный запрос по жанру."""
        genre_uuid = setup_genres[0]['uuid']

        response = await make_request(f'genres/{genre_uuid}')
        assert response.status == http.HTTPStatus.OK
        assert response.body == setup_genres[0]

    @pytest.mark.asyncio
    async def test_genres_detail_404(self, setup_genres, make_request):
        """Запрос отсутствующего жанра."""
        genre_uuid = uuid.uuid4()

        response = await make_request(f'genres/{genre_uuid}')
        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'Genre not found'}

    @pytest.mark.asyncio
    async def test_genres_cache(
            self,
            make_request,
            setup_genres,
            es_client,
            genres_es_index):
        """Тест кеширования."""

        response = await make_request('genres/')

        assert response.status == http.HTTPStatus.OK
        await remove_data_from_es(es_client, genres_es_index, setup_genres)

        second_response = await make_request('genres/')

        assert second_response.status == http.HTTPStatus.OK
