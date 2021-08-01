import json
from flask import Flask, request, jsonify
import boto3
import sys
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.transform import TransformationInjector
from awsresources import MyDB, MySQS

#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

tableName = 'games'
queueName = 'chessdynamics-queue'



@app.route('/games/', methods=['GET'])
def get_all_games():
    db = MyDB(tableName)
    return jsonify(db.get_all())

@app.route('/games/', methods=['POST'])
def create_game():
    q = MySQS(queueName)

    game = json.loads(request.data)
    gamerequest = {
        "function" : "create",
        "game": game
    }
    q.send_message(gamerequest)
    return jsonify("successfully added create task to queue")


@app.route('/games/<game_id>/', methods=['PUT'])
def update_game():
    q = MySQS(queueName)

    game = json.loads(request.data)
    game["id"] = game_id
    gamerequest = {
        "function" : "edit",
        "game": game,
    }
    q.send_message(gamerequest)
    return jsonify("successfully added edit task to queue")


@app.route('/games/<game_id>/', methods=['GET'])
def get_game(game_id):
    db = MyDB(tableName)
    return jsonify(db.download(game_id))
    
@app.route('/games/', methods=['DELETE'])
def delete_game():
    q = MySQS(queueName)

    game = json.loads(request.data)
    game["id"] = game_id
    gamerequest = {
        "function" : "delete",
        "game": game,
    }
    q.send_message(gamerequest)
    return jsonify("successfully added delete task to queue")


@app.route('/games/<game_id>/play_turn/', methods=['PUT', 'POST', 'GET'])
def play_turn(game_id):
    q = MySQS(queueName)
    gamerequest = {
        "function" : "play_turn",
        "game": {
            "id" : game_id
        },
    }
    q.send_message(gamerequest)
    return jsonify("successfully added play_turn task to queue")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)