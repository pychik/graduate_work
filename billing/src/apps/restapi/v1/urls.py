from apps.restapi.v1.views import SubscribeView
from django.urls import path


urlpatterns = [
    path('subscriptions/', SubscribeView.as_view(), name='subscriptions'),
]
