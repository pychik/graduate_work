from unittest import mock

from apps.offer.models import Subscription
from apps.restapi.tests.base import BaseApiTestCase
from apps.restapi.tests.data_factories import TransactionFactory
from apps.restapi.tests.utils import reverse_with_query_params
from apps.restapi.v1.views import NewTransactionView, TransactionDetailView, TransactionListView
from apps.transactions.models import Transaction, UserSubscription
from django.shortcuts import reverse


class TransactionTestCase(BaseApiTestCase):

    # def setUp(self) -> None:
    #     TransactionFactory.create_batch(50)

    def test_transaction_detail(self):
        transaction = TransactionFactory.create()

        view = TransactionDetailView
        view_kwargs = {'guid': transaction.guid}
        url = reverse('single-transaction', kwargs=view_kwargs)
        response = self.call_get_api(view=view, view_kwargs=view_kwargs, url=url, expected_code=200, json_result=True)
        expected = dict(guid=str(transaction.guid),
                        user_id=transaction.user_id,
                        status=transaction.status,
                        subscription=transaction.subscription.name)
        self.assertEqual(response, expected)

    def test_user_transaction(self):
        """
        Тест проверяющий, что /user_transactions/
        отдает только транзакции конкретного пользователя
        """

        # Создадим несколько случайных транзакций
        TransactionFactory.create_batch(25)

        # Создадим транзакции конкретного юзера
        user_id = 1234554321
        user_transactions = TransactionFactory.create_batch(25, **{'user_id': user_id})

        data = {'user_id': user_id}

        view = TransactionListView
        url = reverse('user_transactions')
        response = self.call_post_api(view=view, url=url, expected_code=200, data=data, json_result=True)

        # Сравним количество транзакций пользователя в ответе и созданных
        expected = len(user_transactions)
        self.assertEqual(len(response.get('results')), expected)

    def test_user_transactions_pagination(self):
        user_id = 1234554321
        TransactionFactory.create_batch(100, **{'user_id': user_id})
        data = {'user_id': user_id}
        page = 2
        page_size = 5
        query_params = dict(page=page, page_size=page_size)
        view = TransactionListView
        url = reverse_with_query_params('user_transactions', query_params=query_params)
        response = self.call_post_api(view=view, url=url, expected_code=200, data=data, json_result=True)
        response_len = len(response.get('results'))
        self.assertEqual(response_len, page_size)

    def test_transaction_create(self):
        subscription = Subscription.objects.first()
        view = NewTransactionView
        user_id = 1234554321
        data = {'user_id': user_id, 'subscription_id': str(subscription.guid), 'period': 'months', 'periods_number': 5}
        url = reverse('new-transaction')

        with mock.patch('apps.transactions.utility.payment.YookassaBilling.create_payment') as payment_mock:
            payment_mock.return_value = {
                'amount': {'currency': 'RUB', 'value': 2800.0}, 'confirmation': {
                    'confirmation_url': 'https://yoomoney.ru/checkout/payments/'
                                        'v2/contract?orderId=2ac23bfb-000f-5000-8000-169f4bc99e17',
                    'return_url': 'http://127.0.0.1:7777', 'type': 'redirect'},
                'created_at': '2022-09-25T10:06:51.904Z',
                'description': 'test',
                'id': '2ac23bfb-000f-5000-8000-169f4bc99e17',
                'metadata': {}, 'paid': False,
                'payment_method': {'id': '2ac23bfb-000f-5000-8000-169f4bc99e17',
                                   'saved': False, 'type': 'bank_card'},
                'recipient': {'account_id': '940659', 'gateway_id': '1998643'},
                'refundable': False, 'status': 'pending', 'test': True}

            response = self.call_post_api(view=view, url=url, expected_code=201, data=data, json_result=True)
        transaction_id = response.get('transaction_id')
        self.assertTrue(Transaction.objects.filter(guid=transaction_id).exists())
        self.assertTrue(UserSubscription.objects.filter(transaction__guid=transaction_id).exists())
        self.assertTrue(response.get('url'))
        self.assertTrue(response.get('transaction_id'))
