import boto3
import json

class MySQS:
    def __init__(self, name, region="us-west-2"):
        self.region = region
        self.name = name
        self.client = boto3.client("sqs", region_name=self.region)
        self.queue_url = self.get_queue_url()

    def get_queue_url(self):
        response = self.client.get_queue_url(
            QueueName=self.name,
        )
        return response["QueueUrl"]

    def purge_queue(self):
        response = self.client.purge_queue(
            QueueUrl=self.queue_url,
        )
        return response

    def count(self):
        response = self.client.get_queue_attributes(
            QueueUrl=self.queue_url,
            AttributeNames=[
                'ApproximateNumberOfMessages'
            ]
        )
        return int(response['Attributes']['ApproximateNumberOfMessages'])

    def receive_message(self, waitTime=5):
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=waitTime,
        )
        if 'Messages' not in response:
            return None
        messages = response['Messages']
        message = messages[0]
        receipt_handle = message['ReceiptHandle']
        self.delete_message(receipt_handle)
        return message['Body']

    def send_message(self, message):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message,
            MessageGroupId="string",
            MessageDeduplicationId="string"
        )

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
