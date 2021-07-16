from django.core.management.base import BaseCommand, CommandError
from chessapp.models import Game
from chessapp.chessdynamics import GameModel
from django.contrib.auth.models import User
import boto3
import json

QUEUE_NAME = ""
AWS_REGION = ""

class Command(BaseCommand):
    help = "Consume objects from sqs"

    def add_arguments(self, parser):
        pass

def get_queue_url():
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)
    response = sqs_client.get_queue_url(
        QueueName=QUEUE_NAME,
    )
    return response["QueueUrl"]

def receive_message(messageCount=10, waitTime=5):
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)
    responseUrl = sqs_client.get_queue_url(
        QueueName=QUEUE_NAME,
    )
    queueURL = responseUrl["QueueUrl"]
    response = sqs_client.receive_message(
        QueueUrl=queueURL,
        MaxNumberOfMessages=messageCount,
        WaitTimeSeconds=waitTime,
    )
    return response.get("Messages", [])

def delete_message(receipt_handle):
    sqs_client = boto3.client("sqs", region_name="us-west-2")
    response = sqs_client.delete_message(
        QueueUrl="https://us-west-2.queue.amazonaws.com/xxx/my-new-queue",
        ReceiptHandle=receipt_handle,
    )

    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {json.loads(message_body)}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")


    def handle(self, *args, **options):
        sqs_client = boto3.client("sqs", region_name="us-west-2")
        while True:
            messages = receive_message()
            for message in messages:
                message_body = message["Body"]
                self.stdout.write(self.style.SUCCESS(f"Message body: {json.loads(message_body)}")
                delete_message(message['ReceiptHandle'])
        self.stdout.write(self.style.SUCCESS("Finished consuming!"))
