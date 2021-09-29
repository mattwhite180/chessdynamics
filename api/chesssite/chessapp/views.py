from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os
from chessapp.models import Game
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chessapp.serializers import GameSerializer
from chessapp.chessdynamics import GameHandler, Stockfish, Leela
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
    This is the RESTful API for Chessdynamics
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True)
    def play_leela(self, request, *args, **kwargs):
        game = self.get_object()
        if game.available:
            gh = GameHandler(game)
            s = Leela(game.time_controls)
            move = s.getMove(gh.get_board())
            # move = gh.play_turn()
            gh.play_move(move)
            return Response(
                {
                    "message": "game " + str(game.id) + " moved",
                    "move": move,
                    "gameover": str(gh.is_game_over()),
                }
            )
        else:
            return Response({"message": "game is already in use"})

    @action(detail=True, url_path="play_stockfish/(?P<level_str>[^/.]+)")
    def play_stockfish(self, request, level_str, pk=None):
        game = self.get_object()
        if game.available:
            gh = GameHandler(game)
            s = Stockfish(int(level_str), game.time_controls)
            move = s.getMove(gh.get_board())
            # move = gh.play_turn()
            gh.play_move(move)
            return Response(
                {
                    "message": "game " + str(game.id) + " moved",
                    "move": move,
                    "gameover": str(gh.is_game_over()),
                }
            )
        else:
            return Response({"message": "game is already in use"})
    # @action(detail=True)
    # def play_continuous(self, request, *args, **kwargs):
    #     game = self.get_object()
    #     if game.available:
    #         gh = GameHandler(game)
    #         moves = gh.play_continuous()
    #         return Response(
    #             {
    #                 "message": "game " + str(game.id) + " moved",
    #                 "moves": moves,
    #                 "gameover": str(gh.is_game_over()),
    #             }
    #         )
    #     else:
    #         return Response({"message": "game is already in use"})

    @action(detail=True, url_path="play_move/(?P<move_str>[^/.]+)")
    def play_move(self, request, move_str, pk=None):
        game = self.get_object()
        if game.available:
            gh = GameHandler(game)
            valid_move = gh.play_move(str(move_str))
            return Response({"valid move": valid_move})
        else:
            return Response({"message": "game is already in use"})

    @action(detail=True, url_path="echo/(?P<string>[^/.]+)")
    def echo(self, request, string, pk=None):
        return Response({"message": "echo returns " + string})

    @action(detail=True)
    def pop(self, request, *args, **kwargs):
        game = self.get_object()
        if game.available:
            gh = GameHandler(game)
            move = gh.pop()
            return Response({"message": "pop " + move + " from " + str(game.id)})
        else:
            return Response({"message": "game is already in use"})

    def perform_create(self, serializer):
        serializer.save()
