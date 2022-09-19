from apps.restapi.v1.views import SubscribesView, TransactionDetailView, TransactionsView
from django.urls import path


urlpatterns = [
    path('subscriptions/', SubscribesView.as_view(), name='subscriptions'),
    path('new_transaction/', TransactionsView.as_view(), name='new-transaction'),
    path('transaction/<guid>/', TransactionDetailView.as_view(), name='single-transaction'),
]
