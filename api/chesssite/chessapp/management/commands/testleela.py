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
        for i in User.objects.all():
            i.delete()
        for i in Game.objects.all():
            i.delete()
        mattw = User.objects.create_user("mattw", password="asdf")
        mattw.is_superuser = True
        mattw.is_staff = True
        mattw.save()

        leela = Game.objects.create(
            name="leelatest", white="stockfish", white_level=8, black="leela", time_controls=(2 * 1000)
        )
        
        l = GameModel(leela)

        while l.is_game_over() == False:
            m = l.play_turn()
            print(l.print_game())
            print("############")
        print(l.get_results())