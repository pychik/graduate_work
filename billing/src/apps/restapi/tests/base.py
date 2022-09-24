import json

from rest_framework.test import APIRequestFactory, APITestCase


class BaseApiTestCase(APITestCase):
    factory = APIRequestFactory()

    def call_get_api(self, view, url, view_kwargs=None, expected_code=200, json_result=False):
        return self._call_api(view, url, view_kwargs=view_kwargs, data=None, expected_code=expected_code,
                              method='GET', json_result=json_result)

    def call_post_api(self, view, url, data, view_kwargs=None, expected_code=201, json_result=False):
        return self._call_api(view, url, view_kwargs=view_kwargs, data=data, expected_code=expected_code,
                              method='POST', json_result=json_result)

    def _call_api(self, view, url, view_kwargs=None, data=None, expected_code=201, method='POST', json_result=False):
        json_data = json.dumps(data) if data else None

        factory_method = getattr(self.factory, method.lower())
        request = factory_method(path=url,
                                 content_type='application/json', data=json_data)
        response = view.as_view()(request, **(view_kwargs or {}))
        response_data = response.rendered_content
        self.assertEqual(response.status_code, expected_code)
        if json_result:
            return json.loads(response_data)
        return response_data
