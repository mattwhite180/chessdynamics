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

        self.stdout.write(self.style.SUCCESS("Successfully deleted everything!"))
