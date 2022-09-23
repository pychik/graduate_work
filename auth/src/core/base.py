import json
import logging
from collections import namedtuple

import requests
from core.errors import APIRouterError, InvalidResponseError
from core.helpers import ClientPaginatedResponse, ClientResponse
from flask.json import JSONEncoder
from flask_restx import abort
from models import OauthServices
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from werkzeug.exceptions import GatewayTimeout, PreconditionFailed, ServiceUnavailable


fields = ['host', 'version', 'client_id', 'client_secret']
APICredentials = namedtuple('APICredentials', fields, defaults=(None,) * len(fields))
ClientAPICredentials = namedtuple('APICredentials', fields)


class BaseAPIRouter:
    """
    Базовый роутер
    """
    def __init__(self, *args, **kwargs):
        pass

    def get_credentials(self) -> APICredentials:
        raise NotImplementedError(".get_credentials() must be overridden.")

    def get_base_endpoint(self, **kwargs):
        credentials = self.get_credentials()
        host = credentials.host.rstrip('/')
        return f'{host}/{credentials.version}'

    def get_client_id(self):
        credentials = self.get_credentials()
        return credentials.client_id


class ExternalAPIRouter(BaseAPIRouter):
    _service = None
    _credentials = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = kwargs.get('service')
        self._version = kwargs.get('version')

    def get_credentials(self) -> ClientAPICredentials:
        if not self._credentials:

            if not self._service:
                raise APIRouterError('Select API service!')

            settings = OauthServices.get_service(service=self._service)

            if not settings:
                raise APIRouterError(f'Can\'t get api settings from {self._service}.')

            self._credentials = ClientAPICredentials(
                host=settings.host,
                version=self._version or settings.version,
                client_id=settings.client_id,
                client_secret=settings.client_secret
            )
        return self._credentials


class BaseAPIClient:
    def __init__(self, router: BaseAPIRouter, paginated_response_class=ClientPaginatedResponse,
                 connect_timeout=120, read_timeout=240):
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.router = router
        self.paginated_response_class = paginated_response_class
        self.timeout_params = (self.connect_timeout, self.read_timeout)

    def get_request(self, url, data=None, headers=None):
        response = requests.get(url, params=data, headers=headers, timeout=self.timeout_params)
        return ClientResponse(response)

    def post_request(self, url, data, headers=None, params=None):
        response = requests.post(
            url, data=data, headers=headers, params=params, timeout=self.timeout_params)
        return ClientResponse(response)

    def patch_request(self, url, data, headers=None):
        response = requests.patch(url, data=data, headers=headers, timeout=self.timeout_params)
        return ClientResponse(response)

    def put_request(self, url: str, data: dict, headers: dict = None):
        response = requests.put(url, data=data, headers=headers, timeout=self.timeout_params)
        return ClientResponse(response)

    def delete_request(self, url, data=None, headers=None):
        if data:
            response = requests.delete(url, headers=headers, data=data, timeout=self.timeout_params)
        else:
            response = requests.delete(url, headers=headers, timeout=self.timeout_params)
        return ClientResponse(response)

    @retry(
        retry=retry_if_exception_type((PreconditionFailed, ServiceUnavailable, GatewayTimeout)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _do_make_request(
            self,
            http_method,
            url,
            data=None,
            request_headers=None,
            query_params=None) -> ClientResponse:
        try:
            if http_method == 'GET':
                response = self.get_request(url, headers=request_headers, data=data)
            elif http_method == 'POST':
                response = self.post_request(
                    url, headers=request_headers, data=data, params=query_params)
            elif http_method == 'PATCH':
                response = self.patch_request(url, headers=request_headers, data=data)
            elif http_method == 'PUT':
                response = self.put_request(url, headers=request_headers, data=data)
            elif http_method == 'DELETE':
                response = self.delete_request(url, headers=request_headers, data=data)
            else:
                raise InvalidResponseError(msg='Unsupported HTTP method.')

        except requests.exceptions.RequestException as e:
            abort(code=111, message=str(e))
        return response

    def _make_request(self, http_method, method_url, data=None,
                      request_headers=None, query_params=None, host=None) -> ClientResponse:
        if host:
            url = '{}/{}'.format(host, method_url)
        else:
            url = '{}/{}'.format(self.router.get_base_endpoint(), method_url)
        if data:
            if not request_headers.get('Content-Type', None) == 'application/x-www-form-urlencoded':
                data = json.dumps(data, cls=JSONEncoder)
        try:
            response = self._do_make_request(
                http_method,
                url,
                data=data,
                request_headers=request_headers,
                query_params=query_params
            )
        except Exception as e:
            logging.warning(msg=str(e))
            raise e
        return response

    def method_request(
            self, http_method, url, data=None, headers=None, query_params=None) -> ClientResponse:
        request_headers = {
            'Content-Type': 'application/json'
        }
        request_headers.update(headers or {})
        return self._make_request(
            http_method, url, data, request_headers, query_params=query_params)
