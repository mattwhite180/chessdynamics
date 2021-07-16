import boto3
import json

class MySQS:
    def __init__(self, name, region):
        self.region = region
        self.name = name
        self.client = boto3.client("sqs", region_name=self.region)
        self.queue_url = get_queue_url()

    def get_queue_url(self):
        response = self.client.get_queue_url(
            QueueName=self.name,
        )
        return response["QueueUrl"]

    def send_message(self, message):
        response = self.client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        return response

    def purge_queue(self):
        response = self.client.purge_queue(
            QueueUrl=self.queue_url,
        )
        return response

    def receive_message(self, messageCount=10, waitTime=5):
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=messageCount,
            WaitTimeSeconds=waitTime,
        )
        return response.get("Messages", [])

    def delete_message(self, receipt_handle):
        response = self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle,
        )
        return response

    def change_queue_attributes(self, attributes):
        response = self.client.set_queue_attributes(
            QueueUrl=self.queue_url,
            Attributes=attributes
        )
        return response
