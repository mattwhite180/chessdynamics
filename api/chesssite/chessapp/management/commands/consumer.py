from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.mysqs import MySQS
from chessapp.mydb import MyDB
from chessapp import views
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User
from chessapp.serializers import GameSerializer
import decimal
import boto3
import json
import time

AWS_REGION = "us-west-2"


class Command(BaseCommand):
    help = "Consume objects from sqs"

    def add_arguments(self, parser):
        parser.add_argument("sqs_name", type=str)
        parser.add_argument("db_name", type=str)

    def serialize_game(self, inputgameID, myBool = True):
        inputgame = Game.objects.get(id=inputgameID)
        game_serial = GameSerializer(inputgame)
        game = dict(game_serial.data)
        game_fixed = dict()
        game_fixed["game_id"] = {"N": str(inputgame.id)}
        for i in game:
            if type(game[i]) == type(123):
                game_fixed[i] = {"N": str(game[i])}
            elif type(game[i]) == type(True or False):
                game_fixed[i] = {"BOOL": game[i]}
            else:
                game_fixed[i] = {"S": str(game[i])}
        game_fixed["available"] = { "BOOL": myBool }
        return game_fixed

    def edit_game(self, game_id, gr):
        g = Game.objects.get(id=game_id)
        if "name" in gr:
            g.name = gr["name"]
        if "description" in gr:
            g.description = gr["description"]
        if "move_list" in gr:
            g.move_list = gr["move_list"]
        if "white" in gr:
            g.white = gr["white"]
        if "white_level" in gr:
            g.white_level = gr["white_level"]
        if "black" in gr:
            g.black = gr["black"]
        if "black_level" in gr:
            g.black_level = gr["black_level"]
        if "time_controls" in gr:
            g.time_controls = gr["time_controls"]
        g.save()

    def handleRequest(self, gamerequest, db, sqs):
        if gamerequest["function"] == "create":
            g = Game.objects.create(name="newgame")
            g.save()
            gm = GameModel(g)
            # gm.save()
            gamerequest["game"]["id"] = g.id
            self.edit_game(g.id, gamerequest)
            db.upload(self.serialize_game(g.id))
            gm.delete()
        else:
            # game = Game.objects.get(id=int(gamerequest["game"]["id"]))
            # db.upload(self.serialize_game(game.id, False))
            cloudGame = db.download(int(gamerequest["game"]["id"]))
            print("cloudGame:", cloudGame)
            game = Game.objects.create(name = cloudGame["name"])
            game.description = cloudGame["description"]
            game.move_list = cloudGame["move_list"]
            game.white = cloudGame["white"]
            game.white_level = cloudGame["white_level"]
            game.black = cloudGame["black"]
            game.black_level = cloudGame["black_level"]
            game.time_controls = cloudGame["time_controls"]
            game.results = cloudGame["results"]
            game.available = cloudGame["available"]
            game.turn = cloudGame["turn"]
            game.fen = cloudGame["fen"]
            game.legal_moves = cloudGame["legal_moves"]
            game.creation_date = cloudGame["creation_date"]
            game.save()
            if game.available:
                gm = GameModel(game)
                # gm.save()
                if gamerequest["function"] == "edit":
                    self.edit_game(game_id, gamerequest)
                    db.upload(self.serialize_game(game.id))
                if gamerequest["function"] == "delete":
                    print("im in delete")
                    db.delete_item(game.id)
                if gamerequest["function"] == "play_turn":
                    gm.play_turn()
                    db.upload(self.serialize_game(game.id))
                if gamerequest["function"] == "play_move":
                    gm.play_move(gamerequest["move"])
                    db.upload(self.serialize_game(game.id))
                if gamerequest["function"] == "pop":
                    gm.pop()
                    db.upload(self.serialize_game(game.id))
            gm.delete()

    def handle(self, *args, **options):
        print("hi")
        self.stdout.write(self.style.SUCCESS("Starting consuming!"))
        db = MyDB(options["db_name"], AWS_REGION)
        sqs = MySQS(options["sqs_name"], AWS_REGION)
        # db.delete_item(37)
        # return 0
        sleeptime = 3
        while True:
            time.sleep(sleeptime)
            gamerequest = sqs.receive_message()
            if gamerequest == None:
                sleeptime = 1
                self.stdout.write(self.style.SUCCESS("Finished consuming!"))
            else:
                self.stdout.write(self.style.NOTICE("Finished consuming!"))
                sleeptime = 0
                if "id" in gamerequest["game"]:
                    gameExists = True #Game.objects.filter(id=int(gamerequest["game"]["id"])).exists()
                else:
                    gameExists = False
                createFunction = gamerequest["function"] == "create"
                if (gameExists or createFunction):
                    self.handleRequest(gamerequest, db, sqs)
                else:
                    self.stdout.write(self.style.ERROR("Game ID not found!"))
 