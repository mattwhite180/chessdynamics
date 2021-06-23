from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # path("creategame", views.createGame, name="creategame"),
    path("games/", views.game_list),
    path("games/<int:pk>/", views.game_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)