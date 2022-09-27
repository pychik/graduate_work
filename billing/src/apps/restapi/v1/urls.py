from apps.restapi.v1.views import (
    NewTransactionView,
    PaymentSystemNotification,
    SubscribesView,
    TransactionDetailView,
    TransactionListView,
    TransactionRefundView,
)
from django.urls import path


urlpatterns = [
    path('subscriptions/', SubscribesView.as_view(), name='subscriptions'),
    path('new_transaction/', NewTransactionView.as_view(), name='new-transaction'),
    path('transactions/', TransactionListView.as_view(), name='user_transactions'),
    path('transactions/refund/', TransactionRefundView.as_view(), name='transaction-refund'),
    path('transactions/<guid>/', TransactionDetailView.as_view(), name='single-transaction'),
    path('notifications/', PaymentSystemNotification.as_view(), name='payment-notification'),

]
