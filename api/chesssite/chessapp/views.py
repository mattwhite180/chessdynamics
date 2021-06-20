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


def index(request):
    game_list = Game.objects.order_by("title")
    context = {"game_list": game_list}
    return render(request, "chessapp/index.html", context)


def createGame(request):
    n = os.fork()
    if n > 0:
        post = request.POST
        game = Game(
            title=post.get("game_title", "untitled game"),
            description=post.get("game_description", "not provided"),
            black="stockfish",
            white="stockfish",
            move_list="",
            time_controls=post.get("game_time", 100),
            white_level=post.get("l1", 1),
            black_level=post.get("l2", 1),
        )
        game.save()
        cg = GameModel(game)
        cg.play_continuous()
    else:
        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def game_list(request):
    """
    List all games, or create a new game.
    """
    if request.method == "GET":
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = GameSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def game_detail(request, pk):
    """
    Retrieve, update or delete a code game.
    """
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = GameSerializer(game)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = GameSerializer(game, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        game.delete()
        return HttpResponse(status=204)
