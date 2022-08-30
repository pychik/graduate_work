from django.urls import path
from restapi.v1 import views


urlpatterns = [
    path('likes/', views.LikesView.as_view(), name='notify_likes'),
    path('welcome/', views.WelcomeView.as_view(), name='notify_welcome'),
    path('movie/', views.MovieView.as_view(), name='notify_movie'),
    path('bookmarks/', views.BookmarksView.as_view(), name='notify_bookmarks'),
]
