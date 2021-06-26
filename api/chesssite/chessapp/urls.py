from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # path("creategame", views.createGame, name="creategame"),
    path("", views.api_root),
    path("games/", views.GameList.as_view()),
    path("games/<int:pk>/", views.GameDetail.as_view()),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [path("api-auth/", include("rest_framework.urls"))]
