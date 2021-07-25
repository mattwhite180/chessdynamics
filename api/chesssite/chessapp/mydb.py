import boto3
import json


class MyDB:
    def __init__(self, name, region="us-west-2"):
        self.region = region
        self.name = name
        self.client = boto3.client("dynamodb", region_name=self.region)

    def upload(self, game):
        response = self.client.put_item(
            TableName=self.name, 
            Item=game
        )
    def download(self, id):
        response = self.client.get_item(
        TableName=TABLE_NAME,
        Key={
            'game_id': {'N': id},
            }
        )
        return response['Item']