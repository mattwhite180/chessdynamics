from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os
from chessapp.models import Game
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chessapp.serializers import GameSerializer, UserSerializer
from chessapp.chessdynamics import ChessPlayer, ChessGame, GameModel
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth.models import User
from chessapp.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
import json

@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "games": reverse("game-list", request=request, format=format),
        }
    )

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `play` action.
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    #permission_classes = [(permissions.IsAuthenticatedOrReadOnly&IsOwnerOrReadOnly)|permissions.IsAdminUser]
    # permission_classes = [IsOwnerOrReadOnly|permissions.IsAdminUser]

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)

    # @action(detail=True, permission_classes=[(permissions.IsAuthenticatedOrReadOnly&IsOwnerOrReadOnly)|permissions.IsAdminUser])
    @action(detail=True, permission_classes=[(permissions.IsAuthenticatedOrReadOnly&IsOwnerOrReadOnly)|permissions.IsAdminUser])
    def play(self, request, *args, **kwargs):
        game = self.get_object()
        gm = GameModel(game)
        move = gm.play_turn()
        # serializer = MySerializer(move)
        # response = {}
        # response['success'] = True
        # response['data'] = serializer.data
        return Response({
            'move': str(move.move),
            'gameover': str(gm.is_game_over())})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

