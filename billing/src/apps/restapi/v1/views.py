import http

from apps.offer.models import Subscription, SubscriptionType
from apps.offer.utility.payment import YookassaBilling
from apps.restapi.v1.serializers.offer.subscribe import SubscribeSerialize
from apps.restapi.v1.serializers.offer.transactions import (
    NewTransactionSerializer,
    TransactionSerializer,
)
from apps.transactions.models import Transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.views import APIView, Response


class SubscribesView(APIView):
    """Класс возвращающий данные о подписках."""

    category_response = openapi.Response('response description', SubscribeSerialize(many=True))
    serializer_class = SubscribeSerialize

    @swagger_auto_schema(
        operation_description='Список доступных подписок.',
        responses={
            status.HTTP_200_OK: category_response,
            status.HTTP_400_BAD_REQUEST: 'Bad request'
        }
    )
    def get(self, request):
        subscribes = Subscription.objects.filter(type=SubscriptionType.ENABLE)
        serializer = self.serializer_class(subscribes, many=True)
        return Response(serializer.data)


class TransactionsView(generics.GenericAPIView):
    """
    Класс Api для создания новой транзакции
    """
    serializer_class = NewTransactionSerializer

    @swagger_auto_schema(operation_description='Создание новой транзакции')
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            subscription = Subscription.objects.get(guid=serializer.data.get('subscription_id'))
            price = subscription.price
            payment = YookassaBilling().create_payment(description='test', value=price, payment_type='bank_card')
            url = payment.get('confirmation').get('confirmation_url')
            # тут нужно будет сохранить транзакцию в базу

            return Response(dict(url=url))

        return Response(dict(errors=serializer.errors), status=http.HTTPStatus.BAD_REQUEST)


class TransactionStatusReceiverView:
    """
    Класс API для получения статуса платежа от Юмани
    """
    # TODO: дописать.


class TransactionListView(generics.ListAPIView):
    """
    Класс API для получения данных по всем платежам юзера
    TODO: дописать.
    """


class TransactionDetailView(generics.RetrieveAPIView):
    """
    Класс API для получения данных по конкретному платежу
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'guid'

    @swagger_auto_schema(operation_description='Данные по транзакции')
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
