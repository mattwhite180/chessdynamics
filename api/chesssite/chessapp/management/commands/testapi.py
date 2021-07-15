from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User
import datetime
import time


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        random = Game.objects.create(
            name="apitest",
            description="random vs lvl 1",
            move_list="",
            black="stockfish",
            black_level=1,
            white="random",
            white_level=1,
            time_controls=(10000),
            creation_date=datetime.date(2021, 6, 4),
        )

        one = GameModel(random)
        while not one.is_game_over():
            print("hello!")
            one.play_turn()
        self.stdout.write(self.style.SUCCESS("Successfully setup mock users and games"))
