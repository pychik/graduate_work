from django.urls import include, path


urlpatterns = [
    path('v1/', include('apps.restapi.v1.urls')),
]
