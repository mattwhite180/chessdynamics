from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("creategame", views.createGame, name="creategame"),
    path('games/', views.game_list),
    path('games/<int:pk>/', views.game_detail),
]
