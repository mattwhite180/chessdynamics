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
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth.models import User
from chessapp.permissions import IsOwnerOrReadOnly


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    queryset = Game.objects.all()
    serializer_class = GameSerializer



# def index(request):
#     game_list = Game.objects.order_by("title")
#     context = {"game_list": game_list}
#     return render(request, "chessapp/index.html", context)


# def createGame(request):
#     n = os.fork()
#     if n > 0:
#         post = request.POST
#         game = Game(
#             title=post.get("game_title", "untitled game"),
#             description=post.get("game_description", "not provided"),
#             black="stockfish",
#             white="stockfish",
#             move_list="",
#             time_controls=post.get("game_time", 100),
#             white_level=post.get("l1", 1),
#             black_level=post.get("l2", 1),
#         )
#         game.save()
#         cg = GameModel(game)
#         cg.play_continuous()
#     else:
#         return HttpResponseRedirect(reverse("index"))


# # @csrf_exempt
# @api_view(["GET", "POST"])
# def game_list(request, format=None):
#     """
#     List all games, or create a new game.
#     """
#     if request.method == "GET":
#         games = Game.objects.all()
#         serializer = GameSerializer(games, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = GameSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# @api_view(["GET", "PUT", "DELETE"])
# def game_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code game.
#     """
#     try:
#         game = Game.objects.get(pk=pk)
#     except Game.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = GameSerializer(game)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = GameSerializer(game, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     elif request.method == "DELETE":
#         game.delete()
#         return HttpResponse(status=204)
