from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.mysqs import MySQS
from chessapp.mydb import MyDB
from chessapp import views
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User
from chessapp.serializers import GameSerializer
import boto3
import json
import time

AWS_REGION = "us-west-2"


class Command(BaseCommand):
    help = "Consume objects from sqs"

    def add_arguments(self, parser):
        parser.add_argument("sqs_name", type=str)
        parser.add_argument("db_name", type=str)

    def serialize_game(self, game_id):
        game_serial = GameSerializer(Game.objects.get(id=game_id))
        game = dict(game_serial.data)
        game_fixed = dict()
        game_fixed["game_id"] = {"N": str(game_id)}
        for i in game:
            if type(game[i]) == type(123):
                game_fixed[i] = {"N": str(game[i])}
            elif type(game[i]) == type(True or False):
                game_fixed[i] = {"BOOL": game[i]}
            else:
                game_fixed[i] = {"S": str(game[i])}
        return game_fixed

    def handlerequest(self, gamerequest, db, sqs):
        game = Game.objects.get(id=int(gamerequest["id"]))
        if game.available:
            gm = GameModel(game)
            if gamerequest["function"] == "play_turn":
                gm.play_turn()
            if gamerequest["function"] == "play_move":
                gm.play_move(gamerequest["move"])
            if gamerequest["function"] == "pop":
                gm.pop()

    def handle(self, *args, **options):
        print("hi")
        self.stdout.write(self.style.SUCCESS("Starting consuming!"))
        db = MyDB(options["db_name"], AWS_REGION)
        sqs = MySQS(options["sqs_name"], AWS_REGION)
        sleeptime = 1
        while True:
            time.sleep(sleeptime)
            gamerequest = sqs.receive_message()
            if gamerequest == None:
                sleeptime = 1
                self.stdout.write(self.style.SUCCESS("Finished consuming!"))
            else:
                self.stdout.write(self.style.NOTICE("Finished consuming!"))
                sleeptime = 0
                if Game.objects.filter(id=int(gamerequest["id"])).exists():
                    self.handlerequest(gamerequest, db, sqs)
                else:
                    self.stdout.write(self.style.ERROR("Game ID not found!"))
 