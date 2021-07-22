from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.mysqs import MySQS
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User
import boto3
import json

AWS_REGION = ""

class Command(BaseCommand):
    help = "Consume objects from sqs"

    def add_arguments(self, parser):
        parser.add_argument('sqs_name', type=int)

    def handle(self, *args, **options):
        sqs = MySQS(options['sqs_name'], AWS_REGION)
        while True:
            messages = sqs.receive_message()
            for message in messages:
                message_body = message["Body"]
                self.stdout.write(self.style.SUCCESS(f"Message body: {json.loads(message_body)}")
                sqs.delete_message(message['ReceiptHandle'])
        self.stdout.write(self.style.SUCCESS("Finished consuming!"))
