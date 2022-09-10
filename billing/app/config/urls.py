from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as swagger_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restapi.urls')),
]

urlpatterns += swagger_urls
