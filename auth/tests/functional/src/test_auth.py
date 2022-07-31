from http import HTTPStatus

import pytest
from tests.functional.utils.helper import get_endpoint_url


class TestAuth:

    @pytest.mark.asyncio
    async def test_sign_up(self, make_request):
        url = get_endpoint_url('auth_sign_up')
        method = 'POST'
        data = dict(email='ttestuser@test.com', password='test_password')
        response = await make_request(url, method, data=data)
        assert response.status == HTTPStatus.CREATED

    @pytest.mark.asyncio
    async def test_sign_up_failed(self, make_request):
        url = get_endpoint_url('auth_sign_up')
        method = 'POST'
        # указываем неверные данные
        data = dict(username='test_user', password='test_password')
        response = await make_request(url, method, data=data)
        assert response.status == HTTPStatus.BAD_REQUEST
        assert response.body['errors'] == {'email':
                                           'Email Missing required parameter in the JSON body'}

    @pytest.mark.asyncio
    async def test_login(self, make_request, test_user):
        url = get_endpoint_url('auth_login')
        method = 'POST'
        password = 'Test_password'
        data = dict(email=test_user.email, password=password)
        response = await make_request(url, method, data=data)
        assert response.status == HTTPStatus.OK
        assert response.body.get('access_token')
        assert response.body.get('refresh_token')

    @pytest.mark.asyncio
    async def test_login_failed(self, make_request, test_user):
        url = get_endpoint_url('auth_login')
        method = 'POST'
        wrong_password = 'test_failed_password'
        data = dict(email=test_user.email, password=wrong_password)
        response = await make_request(url, method, data=data)
        assert response.status == HTTPStatus.NOT_FOUND
        assert response.body['errors'] == ['Некорректные данные для авторизации']

    @pytest.mark.asyncio
    async def test_refresh_token(self, make_request, refresh_token):
        url = get_endpoint_url('auth_refresh_token')
        method = 'POST'
        headers = {'Authorization': f'Bearer {refresh_token}'}
        response = await make_request(url, method, headers)
        assert response.status == HTTPStatus.OK
        assert response.body.get('access_token')
