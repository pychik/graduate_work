from django.urls import include, path


urlpatterns = [
    path('v1/billing/', include('restapi.v1.urls')),
]
