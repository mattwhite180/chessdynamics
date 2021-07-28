import boto3
import json


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
        return response["Item"]

    def delete_item(self, id):
        response = self.client.delete_item(
            TableName=self.name, Key={"game_id": {"N": str(id)}}
        )