from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os
from chessapp.models import Game
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chessapp.serializers import GameSerializer
from chessapp.chessdynamics import ChessPlayer, ChessGame, GameModel
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
import json


@api_view(["GET"])
def api_root(request, format=None):
    return Response({"games": reverse("game-list", request=request, format=format)})


class GameViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True)
    def play_turn(self, request, *args, **kwargs):
        # serializer = MySerializer(move)
        # response = {}
        # response['success'] = True
        # response['data'] = serializer.data
        game = self.get_object()
        gm = GameModel(game)
        move = gm.play_turn()
        return Response({"move": move, "gameover": str(gm.is_game_over())})

    @action(detail=True, url_path="play_move/(?P<move_str>[^/.]+)")
    def play_move(self, request, move_str, pk=None):
        game = self.get_object()
        gm = GameModel(game)
        valid_move = gm.play_move(str(move_str))
        return Response({"valid move": valid_move})

    def perform_create(self, serializer):
        serializer.save()
