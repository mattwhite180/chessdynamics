from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import boto3
import json
import sys


class MyDB:
    def __init__(self, name, region="us-west-2"):
        self.region = region
        self.name = name
        self.client = boto3.client("dynamodb", region_name=self.region)

    def download(self, id):
        response = self.client.get_item(
            TableName=self.name, Key={"game_id": {"N": str(id)}}
        )
        if "Item" in response:
            return response["Item"]
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


app = Flask(__name__)
api = Api(app)


def abort_if_game_doesnt_exist(game_id):
    if game_id not in GAMES:
        abort(404, message="Game {} doesn't exist".format(game_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Game
# shows a single game item and lets you delete a game item
class Game(Resource):
    def get(self, game_id):
        abort_if_game_doesnt_exist(game_id)
        return GAMES[game_id]

    def delete(self, game_id):
        abort_if_game_doesnt_exist(game_id)
        del GAMES[game_id]
        return '', 204

    def put(self, game_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        GAMES[game_id] = task
        return task, 201

# GameList
# shows a list of all games, and lets you POST to add new tasks
class GameList(Resource):
    def get(self):
        return GAMES

    def post(self):
        args = parser.parse_args()
        game_id = int(max(GAMES.keys()).lstrip('game')) + 1
        game_id = 'game%i' % game_id
        GAMES[game_id] = {'task': args['task']}
        return GAMES[game_id], 201


##
## Actually setup the Api resource routing here
##
api.add_resource(GameList, '/games/')
api.add_resource(Game, '/games/<game_id>/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)