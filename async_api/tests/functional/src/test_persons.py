import http
import uuid

import pytest
from tests.functional.utils.helpers import remove_data_from_es, transform_persons_data


class TestPersons:

    @pytest.mark.asyncio
    async def test_persons_all(self, make_request, setup_persons):
        """Тест запроса всех персонажей"""

        test_data = transform_persons_data(setup_persons)

        response = await make_request('persons/')

        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == len(test_data)
        assert response.body == test_data

    @pytest.mark.asyncio
    async def test_persons_detail(self, make_request, setup_persons):
        """Тест запроса конкретного персонажа"""

        persons_uuid = setup_persons[0]['uuid']

        response = await make_request(f'persons/{persons_uuid}')

        assert response.status == http.HTTPStatus.OK
        assert response.body == setup_persons[0]

    @pytest.mark.asyncio
    async def test_persons_detail_404(self, make_request, setup_persons):
        """Тест запроса конкретного персонажа, которого нет"""

        persons_uuid = uuid.uuid4()

        response = await make_request(f'persons/{persons_uuid}')

        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'Person not found'}

    @pytest.mark.asyncio
    async def test_persons_list_sorted(self, make_request, setup_persons):
        """Тест запроса персонажей с сортировкой и размером страницы"""

        sorting = 'full_name'
        page_size = 1

        response = await make_request(f'persons/?sort={sorting}&page[size]={page_size}')

        test_data = transform_persons_data(setup_persons)
        sorted_test_data = sorted(test_data, key=lambda x: x[sorting])

        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == page_size
        assert response.body == sorted_test_data[:page_size]

    @pytest.mark.asyncio
    async def test_persons_pagination(self, make_request, setup_persons):
        """Тест пагинации при запросе персонажей"""

        page_size = 1
        page_num = 2

        test_data = transform_persons_data(setup_persons)

        response = await make_request(f'persons/?page[size]={page_size}&page[number]={page_num}')

        assert response.status == http.HTTPStatus.OK
        assert response.body == test_data[page_num - 1: page_num * page_size]

    @pytest.mark.asyncio
    async def test_persons_cache(self, make_request, setup_persons, es_client, persons_es_index):
        """Тест кеширования при запросе персонажей"""

        response = await make_request('persons/')

        assert response.status == http.HTTPStatus.OK
        await remove_data_from_es(es_client, persons_es_index, setup_persons)

        second_response = await make_request('persons/')

        assert second_response.status == http.HTTPStatus.OK
