from django.contrib import admin
from django.urls import path

from .yasg import urlpatterns as swagger_urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += swagger_urls
