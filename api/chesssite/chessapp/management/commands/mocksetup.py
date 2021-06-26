from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        user1=User.objects.create_user('test1', password='test1')
        user1.save()

        user2=User.objects.create_user('test2', password='test2')
        user2.save()

        mattw=User.objects.create_user('mattw', password='asdf')
        mattw.is_superuser=True
        mattw.is_staff=True
        mattw.save()

        simple_checkmate_in_one = Game.objects.create(title="easy checkmate in one", owner=user1)
        one = GameModel(simple_checkmate_in_one)
        one.load_game("e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3")

        new_game = Game.objects.create(title="not played yet", owner=user1)
        
        finished_game = Game.objects.create(title="finished game", owner=user2)
        two = GameModel(finished_game)
        two.play_continuous()

        self.stdout.write(self.style.SUCCESS('Successfully setup mock users and games'))