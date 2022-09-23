from http import HTTPStatus

import pytest
from tests.functional.utils.helper import get_endpoint_url


class TestRoles:

    @pytest.mark.asyncio
    async def test_creating(self, make_request, access_token):
        url = get_endpoint_url('roles')
        method = 'POST'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = dict(name='Admin', description='Rules the world')
        response = await make_request(url, method, headers, data=data)
        assert response.status == HTTPStatus.CREATED
        assert response.body

    @pytest.mark.asyncio
    async def test_get_list(self, make_request, access_token):
        url = get_endpoint_url('roles')
        method = 'GET'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await make_request(url, method, headers)
        assert response.status == HTTPStatus.OK
        assert len(response.body.get('items')) == 2

    @pytest.mark.asyncio
    async def test_get_role(self, make_request, test_role, access_token):
        url = get_endpoint_url('roles-detail', test_role.pk)
        method = 'GET'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await make_request(url, method, headers)
        assert response.status == HTTPStatus.OK
        assert response.body.get('name') == test_role.name
        assert response.body.get('description') == test_role.description

    @pytest.mark.asyncio
    async def test_role_updating(self, make_request, test_role, access_token):
        url = get_endpoint_url('roles-detail', test_role.pk)
        method = 'PUT'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = dict(name='admin', description="Cannot be replaced")
        response = await make_request(url, method, headers, data=data)
        assert response.status == HTTPStatus.OK

    @pytest.mark.asyncio
    async def test_role_deleting(self, make_request, test_role, access_token):
        url = get_endpoint_url('roles-detail', test_role.pk)
        method = 'DELETE'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await make_request(url, method, headers)
        assert response.status == HTTPStatus.NO_CONTENT
