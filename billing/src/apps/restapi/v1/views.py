import http
import logging

from apps.offer.models import Subscription, SubscriptionType
from apps.restapi.errors import NotPaidYetError
from apps.restapi.v1.filters import UserFilterBackend
from apps.restapi.v1.pagination import PageNumberSizePagination
from apps.restapi.v1.serializers.offer.subscribe import SubscribeSerialize
from apps.restapi.v1.serializers.offer.transactions import (
    NewTransactionSerializer,
    RefundSerializer,
    TransactionSerializer,
    UserIdSerializer,
)
from apps.transactions.models import Refund, Transaction, UserSubscription
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

            _transaction = Transaction(user_id=serializer.data.get('user_id'),
                                       subscription=subscription)
            user_subscription = UserSubscription(transaction=_transaction, **serializer.data)

            amount = user_subscription.calculate_amount(set_value=True)
            try:
                payment = YookassaBilling().create_payment(description='test',
                                                           value=amount, currency=subscription.currency,
                                                           payment_type='bank_card')
            except Exception as e:
                logging.error(str(e))
                logging.error('Payment failed')
            else:
                logging.info('Payment successful')

                payment_system_id = payment.get('id')
                _transaction.payment_system_id = payment_system_id
                _transaction.amount = amount
                _transaction.currency = subscription.currency
                _transaction.save()

                user_subscription.currency = subscription.currency
                user_subscription.save()

                url = payment.get('confirmation').get('confirmation_url')
                response_data = dict(url=url, transaction_id=_transaction.guid)
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


class TransactionRefundView(APIView):
    serializer_class = RefundSerializer
    # refund_response = openapi.Response('transactions', RefundSerializer(many=True))
    http_method_names = ['post']

    @swagger_auto_schema(operation_description='Создание возврата по транзакции',
                         operation_id='transaction-refund')
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            _transaction = Transaction.objects.get(guid=serializer.data.get('transaction_id'))
            try:
                amount = _transaction.user_subscription.calculate_refund_amount()
            except NotPaidYetError:
                message = 'Transaction still not paid'
                logging.error(message)
                response_data = dict(error=message)
                status_code = http.HTTPStatus.BAD_REQUEST
            else:
                currency = _transaction.currency  # TODO: куда то положить еще

                refund = YookassaBilling().refund_payment(payment_id=_transaction.payment_system_id,
                                                          amount=amount, currency=currency)
                refund_status = refund.get('status')
                refund_db = Refund(transaction=_transaction,
                                   status=refund_status,
                                   payment_system_id=refund.get('id'),
                                   amount=amount,
                                   currency=currency
                                   )
                if refund_status == 'canceled':
                    response_data = refund.get('cancelation_details')
                    refund_db.cancellation_details = response_data

                else:
                    response_data = dict(status='success', amount=amount)
                refund_db.save()
                status_code = http.HTTPStatus.CREATED
            return Response(data=response_data, status=status_code)

        return Response(data=serializer.errors, status=http.HTTPStatus.BAD_REQUEST)
