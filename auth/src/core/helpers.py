from functools import reduce

from core.errors import InvalidResponseError
from requests import codes
from werkzeug.exceptions import BadRequest, PreconditionFailed, ServiceUnavailable


RATE_LIMIT_CODE = 420  # Enhance your calm


def get_in_dict(c, key_path, default=None):
    def _getter(c, key):
        if c is default:
            return c
        return c.get(key, default)
    return reduce(_getter, key_path.split('.'), c)


class ClientResponse(object):
    def __init__(self, response):
        self._response = response
        if response.status_code >= codes.bad_request:
            if response.status_code == RATE_LIMIT_CODE:
                raise PreconditionFailed
            if response.status_code >= codes.internal_server_error:
                raise ServiceUnavailable
            raise BadRequest

    def __str__(self):
        return self._response.content.decode('utf-8')

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def json(self):
        try:
            if not self._response.text:
                raise InvalidResponseError('Received an empty JSON response')
            return self._response.json()
        except Exception as e:
            return {'error': str(e)}


class ClientPaginatedResponse:
    total_field = 'Meta.total'
    results_field = 'Data'

    def __init__(self, json_response):
        if isinstance(json_response, list):
            self.total = len(json_response)
            self.results = json_response
        else:
            self.total = get_in_dict(json_response, self.total_field) or 0
            self.results = json_response.get(self.results_field) or []
