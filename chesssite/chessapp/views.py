from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os
from .models import Game
from chessapp.chessdynamics import board_to_pgn, playTwoCPU


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
            PGN="",
            time_controls=post.get("game_time", 1),
            black_level=post.get("l1", 1),
            white_level=post.get("l2", 1),
        )
        game.PGN = board_to_pgn(
            playTwoCPU(
                game.white,
                game.black,
                game.white_level,
                game.black_level,
                game.time_controls,
            )
        )
        game.save()
    else:
        return HttpResponseRedirect(reverse("index"))
