import boto3
import json
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.transform import TransformationInjector

class MyDB:
    def __init__(self, name, region="us-west-2"):
        self.region = region
        self.name = name
        self.client = boto3.client("dynamodb", region_name=self.region)

    def upload(self, game_serial):
        response = self.client.put_item(TableName=self.name, Item=game_serial)

    def download(self, id):
        response = self.client.get_item(
            TableName=self.name, Key={"game_id": {"N": str(id)}}
        )
        if "Item" in response:
            deserializer = TypeDeserializer()
            unserialized_item = {k: deserializer.deserialize(v) for k, v in response["Item"].items()}
            return unserialized_item
        else:
            return False

    def delete_item(self, id):
        response = self.client.delete_item(
            TableName=self.name, Key={"game_id": {"N": str(id)}}
        )