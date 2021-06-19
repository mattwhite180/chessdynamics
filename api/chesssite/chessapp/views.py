from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os
from .models import Game
from chessapp.chessdynamics import ChessPlayer, ChessGame


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
            time_controls=post.get("game_time", 100),
            white_level=post.get("l1", 1),
            black_level=post.get("l2", 1),
        )
        whiteEngine = ChessPlayer(
            game.white, game.time_controls, game.white_level, None
        )
        blackEngine = ChessPlayer(
            game.black, game.time_controls, game.black_level, None
        )
        cg = ChessGame(whiteEngine, blackEngine, game.title)
        cg.play_continuous()
        game.PGN = cg.get_PGN()
        game.save()
    else:
        return HttpResponseRedirect(reverse("index"))
