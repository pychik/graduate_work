from apps.restapi.v1.views import (
    NewTransactionView,
    SubscribesView,
    TransactionDetailView,
    TransactionListView,
)
from django.urls import path


urlpatterns = [
    path('subscriptions/', SubscribesView.as_view(), name='subscriptions'),
    path('new_transaction/', NewTransactionView.as_view(), name='new-transaction'),
    path('transactions/', TransactionListView.as_view(), name='user_transactions'),
    path('transaction/<guid>/', TransactionDetailView.as_view(), name='single-transaction'),
]
