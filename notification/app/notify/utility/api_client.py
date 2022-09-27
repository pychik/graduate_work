import logging
import requests

from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApiClient:

    @staticmethod
    def _get_request(url: str):
        try:
            return requests.get(url=url)
        except Exception as e:
            logger.exception(f"ApiClient sending log to Kafka:"
                             f" \'_get_request\' got Exception : {e}")
            return None

    @staticmethod
    def _post_request(url: str, headers: dict = None, data: dict = None):
        try:
            return requests.post(url=url, headers=headers, json=data)
        except Exception as e:
            logger.exception(f"ApiClient sending log to Kafka:"
                             f" \'_post_request\' got Exception: {e}")
            return None

    def request_auth(self, user_id: int):
        _url = settings.AUTH_URL
        _headers = {'api_key': settings.API_KEY}
        _data = {'user_id': user_id}
        _response = self._post_request(url=_url, headers=_headers, data=_data)
        return _response.json()
