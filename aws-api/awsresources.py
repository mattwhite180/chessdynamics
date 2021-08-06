import boto3
import json
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.transform import TransformationInjector
import decimal

class MyDB:
    def __init__(self, name, region="us-west-2"):
        self.region = region
        self.name = name
        self.client = boto3.client("dynamodb", region_name=self.region)

    def get_all(self):
        results = []
        last_evaluated_key = None
        while True:
            if last_evaluated_key:
                response = self.client.scan(
                    TableName=self.name,
                    ExclusiveStartKey=last_evaluated_key
                )
            else: 
                response = self.client.scan(TableName=self.name)
            last_evaluated_key = response.get('LastEvaluatedKey')
            
            results.extend(response['Items'])
            
            if not last_evaluated_key:
                break
        unserialized_items = list()
        deserializer = TypeDeserializer()
        for i in results:
            unserialized_items.append({k: deserializer.deserialize(v) for k, v in i.items()})
        for i in range(len(unserialized_items)):
            for val in unserialized_items[i]:
                if type(unserialized_items[i][val]) == type(decimal.Decimal(1.23)):
                    unserialized_items[i][val] = int(unserialized_items[i][val])
        return unserialized_items

    def download(self, id):
        response = self.client.get_item(
            TableName=self.name, Key={"game_id": {"N": str(id)}}
        )
        if "Item" in response:
            deserializer = TypeDeserializer()
            unserialized_item = {k: deserializer.deserialize(v) for k, v in response["Item"].items()}
            for i in unserialized_item:
                if type(unserialized_item[i]) == type(decimal.Decimal(1.23)):
                    unserialized_item[i] = int(unserialized_item[i])
            return unserialized_item
        else:
            return {"error": "item of ID (" + str(id) + ") not found..."}

class MySQS:
    def __init__(self, name, region="us-west-2"):
        self.region = region
        self.name = name
        self.client = boto3.client("sqs", region_name=self.region)
        self.queue_url = self.get_queue_url()

    def get_queue_url(self):
        response = self.client.get_queue_url(QueueName=self.name)
        return response["QueueUrl"]

    def send_message(self, message):
        response = self.client.send_message(
            QueueUrl=self.queue_url, MessageBody=json.dumps(message)
        )