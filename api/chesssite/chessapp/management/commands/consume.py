from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.mysqs import MySQS
from chessapp.mydb import MyDB
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User
from chessapp.serializers import GameSerializer
import boto3
import json

AWS_REGION = ""

class Command(BaseCommand):
    help = "Consume objects from sqs"

    def add_arguments(self, parser):
        parser.add_argument('sqs_name', type=str)
        parser.add_argument('db_name', type=str)

    def serialize_game(self, game_id):
        game_serial = GameSerializer(Game.objects.get(id=game_id))
        game = dict(game_serial.data)
        game_fixed = dict()
        game_fixed["game_id"] = { 'N' : str(game_id)}
        for i in game:
            if type(game[i]) == type(123):
                game_fixed[i] = { 'N' : str(game[i]) }
            elif type(game[i]) == type(True or False):
                game_fixed[i] = { 'BOOL' : game[i] }
            else:
                game_fixed[i] = { 'S' : str(game[i]) }
        return game_fixed

    # def handle(self, *args, **options):
    #     sqs = MySQS(options['sqs_name'], AWS_REGION)
    #     while True:
    #         messages = sqs.receive_message()
    #         for message in messages:
    #             message_body = message["Body"]
    #             self.stdout.write(self.style.SUCCESS(f"Message body: {json.loads(message_body)}")
    #             sqs.delete_message(message['ReceiptHandle'])
    #     self.stdout.write(self.style.SUCCESS("Finished consuming!"))

    def handle(self, *args, **options):
        db = MyDB(options['db_name'], 'us-west-2')
        gs = self.serialize_game(5)
        self.stdout.write(self.style.SUCCESS("type: " + str(type(gs))))
        for i in gs:
            print(i, ":", gs[i])
        db.upload(gs)
        self.stdout.write(self.style.SUCCESS("Wrote to dynamodb"))
