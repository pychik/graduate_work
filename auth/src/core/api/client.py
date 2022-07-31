from core.base import BaseAPIClient
from core.consts import YANDEX_HOST_INFO
from core.helpers import ClientResponse
from flask import request, url_for


class ApiRestClient(BaseAPIClient):

    def method_request(
            self,
            http_method,
            method_url,
            data=None,
            headers=None,
            query_params=None,
            host=None) -> ClientResponse:
        request_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        request_headers.update(headers or {})
        return self._make_request(
            http_method,
            f'{method_url}',
            data,
            request_headers,
            query_params=query_params,
            host=host
        )

    def get_yandex_user_credentials(self, secret_code: str):
        settings = self.router.get_credentials()
        data = dict(
            grant_type='authorization_code',
            code=secret_code,
            client_id=settings.client_id,
            client_secret=settings.client_secret
        )
        response = self.method_request('POST', 'token', data=data)
        return response.json

    def get_yandex_user_info(self, access_token: str):
        host = YANDEX_HOST_INFO
        headers = {'Authorization': f'OAuth {access_token}'}
        response = self.method_request('GET', 'info', host=host, headers=headers)
        return response.json

    def get_vk_user_credentials(self, code: str):
        settings = self.router.get_credentials()

        redirect_uri = url_for('api.vk-authorize').lstrip('/')
        redirect_uri = f'{request.host_url}{redirect_uri}'
        data = dict(client_id=settings.client_id,
                    client_secret=settings.client_secret,
                    redirect_uri=redirect_uri,
                    code=code)
        response = self.method_request('GET', 'access_token', data=data)
        return response.json
