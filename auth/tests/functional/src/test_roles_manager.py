from http import HTTPStatus

import pytest
from tests.functional.utils.helper import get_endpoint_url


class TestRolesManager:

    @pytest.mark.asyncio
    async def test_adding_role_to_user(self, make_request, test_user, test_role, access_token):
        url = get_endpoint_url('roles-access')
        method = 'POST'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = dict(user_pk=test_user.pk, role=test_role.name)
        response = await make_request(url, method, headers, data)
        assert response.status == HTTPStatus.OK

        url = get_endpoint_url('roles-check')
        response = await make_request(url, method, headers, data)
        assert response.status == HTTPStatus.OK
        assert response.body.get('message')

    @pytest.mark.asyncio
    async def test_delete_role_from_user(self,
                                         make_request,
                                         test_user,
                                         test_role,
                                         access_token,
                                         other_access_token):
        url = get_endpoint_url('roles-access')
        method = 'DELETE'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = dict(user_pk=test_user.pk, role=test_role.name)
        response = await make_request(url, method, headers, data)
        assert response.status == HTTPStatus.NO_CONTENT

        url = get_endpoint_url('roles-check')
        method = 'POST'
        headers = {'Authorization': f'Bearer {other_access_token}'}
        response = await make_request(url, method, headers, data)
        assert response.status == HTTPStatus.OK
        assert not response.body.get('message')
