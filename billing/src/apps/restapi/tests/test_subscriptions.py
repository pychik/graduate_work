import http

from apps.offer.models import Subscription
from apps.restapi.tests.base import BaseApiTestCase
from apps.restapi.v1.views import SubscribesView
from django.shortcuts import reverse


class SubscriptionsTestCase(BaseApiTestCase):

    def tearDown(self) -> None:
        Subscription.objects.all().delete()

    def test_get_subscriptions(self):
        view = SubscribesView
        url = reverse('subscriptions')

        response = self.call_get_api(view=view, url=url, expected_code=http.HTTPStatus.OK, json_result=True)
        expected = [dict(guid=str(sub.guid),
                         name=sub.name,
                         description=sub.description,
                         type=sub.type, price=str(sub.price),
                         currency=sub.currency) for sub in Subscription.objects.all()]

        self.assertEqual(response, expected)
