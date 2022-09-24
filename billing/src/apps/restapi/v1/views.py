import http

from apps.offer.models import Subscription, SubscriptionType
from apps.restapi.v1.filters import UserFilterBackend
from apps.restapi.v1.pagination import PageNumberSizePagination
from apps.restapi.v1.serializers.offer.subscribe import SubscribeSerialize
from apps.restapi.v1.serializers.offer.transactions import (
    NewTransactionSerializer,
    TransactionSerializer,
    UserIdSerializer,
)
from apps.transactions.models import Transaction
from apps.transactions.utility.payment import YookassaBilling
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, status
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
            try:
                payment = YookassaBilling().create_payment(description='test', value=price, payment_type='bank_card')
            except Exception as e:
                print(e)
            else:
                payment_system_id = payment.get('id')
                url = payment.get('confirmation').get('confirmation_url')
                # тут нужно будет сохранить транзакцию в базу
                transaction = Transaction.objects.create(payment_system_id=payment_system_id, **serializer.data)
                response_data = dict(url=url, transaction_id=transaction.guid)
                return Response(data=response_data, status=http.HTTPStatus.CREATED)

        return Response(dict(errors=serializer.errors), status=http.HTTPStatus.BAD_REQUEST)


class TransactionListView(generics.GenericAPIView):
    """
    Класс API для получения данных по всем платежам юзера
    """
    queryset = Transaction.objects.all()
    serializer_class = UserIdSerializer
    filter_backends = [UserFilterBackend, filters.OrderingFilter]
    pagination_class = PageNumberSizePagination
    http_method_names = ['post']
    transaction_response = openapi.Response('transactions', TransactionSerializer(many=True))
    ordering_fields = ['-created_at']
    ordering = ['-created_at']

    @swagger_auto_schema(operation_description='Получение транзакций по user_id',
                         operation_id='user_transactions',
                         responses={
                             status.HTTP_200_OK: transaction_response})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            transactions = self.filter_queryset(self.get_queryset())
            paginated_queryset = self.paginate_queryset(transactions)
            data = TransactionSerializer(paginated_queryset, many=True)
            paginated_response = self.get_paginated_response(data=data.data)

            return paginated_response
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
