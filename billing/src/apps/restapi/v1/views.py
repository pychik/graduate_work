import http

from apps.offer.models import Subscription, SubscriptionType
from apps.offer.utility.payment import YookassaBilling
from apps.restapi.v1.filters import UserFilterBackend
from apps.restapi.v1.serializers.offer.subscribe import SubscribeSerialize
from apps.restapi.v1.serializers.offer.transactions import (
    NewTransactionSerializer,
    TransactionSerializer,
    UserIdSerializer,
)
from apps.transactions.models import Transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
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


class NewTransactionView(generics.GenericAPIView):
    """
    Класс Api для создания новой транзакции
    """
    serializer_class = NewTransactionSerializer

    @swagger_auto_schema(operation_description='Создание новой транзакции',
                         operation_id='transaction_new')
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
    """
    queryset = Transaction.objects.all()
    serializer_class = UserIdSerializer
    filter_backends = [UserFilterBackend]
    pagination_class = PageNumberPagination
    http_method_names = ['post']
    transaction_response = openapi.Response('transactions', TransactionSerializer(many=True))

    @swagger_auto_schema(operation_description='Получение транзакций по user_id',
                         operation_id='user_transactions',
                         responses={
                             status.HTTP_200_OK: transaction_response})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            transactions = self.filter_queryset(self.get_queryset())
            data = TransactionSerializer(transactions, many=True)

            return Response(data.data, status=http.HTTPStatus.OK)
        return Response(serializer.errors, status=http.HTTPStatus.BAD_REQUEST)


class TransactionDetailView(generics.RetrieveAPIView):
    """
    Класс API для получения данных по конкретному платежу
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'guid'

    @swagger_auto_schema(operation_description='Данные по транзакции',
                         operation_id='single-transaction')
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
