from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User
import datetime
import time


class Command(BaseCommand):
    help = "setup mock users and games"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for i in User.objects.all():
            i.delete()
        for i in Game.objects.all():
            i.delete()
        mattw = User.objects.create_user("mattw", password="asdf")
        mattw.is_superuser = True
        mattw.is_staff = True
        mattw.save()

        new_game1 = Game.objects.create(
            name="new1", creation_date=datetime.date(2021, 6, 1), time_controls=(10000)
        )

        new_game2 = Game.objects.create(
            name="new2", creation_date=datetime.date(2021, 6, 2), time_controls=(9000)
        )

        new_game3 = Game.objects.create(
            name="newmattw",
            creation_date=datetime.date(2021, 6, 3),
            time_controls=(8000),
        )

        new_game4 = Game.objects.create(
            name="longgame",
            creation_date=datetime.date(2020, 6, 3),
            time_controls=(7000),
        )

        leela = Game.objects.create(
            name="leela",
            white="stockfish",
            white_level=8,
            black="leela",
            time_controls=(6000),
        )

        Game.objects.create(
            name="random",
            description="random vs lvl 1",
            move_list="",
            black="random",
            black_level=1,
            white="random",
            white_level=8,
            time_controls=(1000),
            creation_date=datetime.date(2021, 6, 4),
        )

        simple_checkmate_in_one = Game.objects.create(
            name="easy checkmate in one", creation_date=datetime.date(2021, 6, 5)
        )
        one = GameModel(simple_checkmate_in_one)
        one.load_game("e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3")

        finished_game = Game.objects.create(
            name="finished game", creation_date=datetime.date(2021, 6, 6)
        )
        two = GameModel(finished_game)
        two.load_game("e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,f3f7")

        finished_random = Game.objects.create(
            name="random finished",
            description="random vs lvl 1",
            move_list="",
            black="stockfish",
            black_level=1,
            white="random",
            white_level=8,
            time_controls=100,
            creation_date=datetime.date(2021, 6, 4),
        )
        three = GameModel(finished_random)
        three.play_continuous()
        self.stdout.write(self.style.SUCCESS("Successfully setup mock users and games"))
