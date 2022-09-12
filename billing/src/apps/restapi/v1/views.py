from apps.offer.models import Subscription
from apps.restapi.v1.serializers.offer.subscribe import SubscribeSerialize
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView, Response


class SubscribeView(APIView):
    """Класс возвращающий данные о подписках."""

    category_response = openapi.Response('response description', SubscribeSerialize(many=True))
    serializer_class = SubscribeSerialize

    @swagger_auto_schema(
        operation_description='Список доуступных подписок.',
        responses={
            status.HTTP_200_OK: category_response,
            status.HTTP_400_BAD_REQUEST: 'Bad request'
        }
    )
    def get(self, request):
        subscribes = Subscription.objects.filter(type=Subscription.SubscriptionType.ENABLE)
        serializer = self.serializer_class(subscribes, many=True)
        return Response(serializer.data)
