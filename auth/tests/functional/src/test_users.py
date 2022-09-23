from http import HTTPStatus

import pytest
from tests.functional.utils.helper import get_endpoint_url


class TestUsers:

    @pytest.mark.asyncio
    async def test_profile(self, make_request, access_token, test_user):
        url = get_endpoint_url('users_profile')
        method = 'GET'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await make_request(url, method, headers)
        assert response.status == HTTPStatus.OK
        assert response.body.get('profile').get('email') == test_user.email

    @pytest.mark.asyncio
    async def test_profile_password(self, make_request, access_token, test_user):
        url = get_endpoint_url('users_profile')
        method = 'PUT'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = dict(old_password='Test_password', new_password='new_test_password')
        response = await make_request(url, method, headers, data)
        assert response.status == HTTPStatus.OK

    @pytest.mark.asyncio
    async def test_profile_password_invalid(self, make_request, access_token):
        url = get_endpoint_url('users_profile')
        method = 'PUT'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = dict(old_password='invalid', new_password='new_test_password')
        response = await make_request(url, method, headers, data)
        assert response.status == HTTPStatus.NOT_FOUND
        assert response.body.get('errors') == ['Указан не верный пароль учетной записи!']

    @pytest.mark.asyncio
    async def test_profile_sessions(self, make_request, access_token, test_user):
        url = get_endpoint_url('auth_login')
        method = 'POST'
        password = 'Test_password'
        data = dict(email=test_user.email, password=password)
        await make_request(url, method, data=data)

        url = get_endpoint_url('users_profile_sessions')
        method = 'GET'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await make_request(url, method, headers)
        assert response.status == HTTPStatus.OK
        assert response.body.get('items')
