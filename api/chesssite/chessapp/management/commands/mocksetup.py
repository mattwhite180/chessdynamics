from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for i in User.objects.all():
            i.delete()
        for i in Game.objects.all():
            i.delete()

        user1 = User.objects.create_user("test1", password="test1")
        user1.is_superuser = False
        user1.is_staff = False
        user1.save()

        user2 = User.objects.create_user("test2", password="test2")
        user2.is_superuser = False
        user2.is_staff = False
        user2.save()

        mattw = User.objects.create_user("mattw", password="asdf")
        mattw.is_superuser = True
        mattw.is_staff = True
        mattw.save()

        new_game1 = Game.objects.create(title="new1", owner=user1)
        new_game2 = Game.objects.create(title="new2", owner=user2)
        new_game3 = Game.objects.create(title="newmattw", owner=mattw)

        Game.objects.create(
            title="random",
            description="random vs lvl 1",
            move_list="",
            black="stockfish",
            black_level=1,
            white="random",
            white_level=8,
            time_controls=100,
            owner=user1,
        )

        simple_checkmate_in_one = Game.objects.create(
            title="easy checkmate in one", owner=user1
        )
        one = GameModel(simple_checkmate_in_one)
        one.load_game("e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3")

        finished_game = Game.objects.create(title="finished game", owner=user2)
        two = GameModel(finished_game)
        two.load_game("e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,f3f7")

        self.stdout.write(self.style.SUCCESS("Successfully setup mock users and games"))
