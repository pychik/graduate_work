from apps.restapi.v1.views import SubscribesView, TransactionsView
from django.urls import path


urlpatterns = [
    path('subscriptions/', SubscribesView.as_view(), name='subscriptions'),
    path('new_transaction/', TransactionsView.as_view(), name='transactions'),
]
