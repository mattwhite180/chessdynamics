# https://flask-restful.readthedocs.io/en/latest/quickstart.html
# https://www.tutorialspoint.com/python_network_programming/python_http_client.htm

import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

    # some_json=request.get_json()
    # return jsonify({'you sent ':some_json})

# Game
# shows a single game item and lets you delete a game item
class Games(Resource):
    def get(self):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (json.loads(requests.get(url).content))

    def delete(self):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (json.loads(requests.delete(url).content))

    def put(self):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (jsonify(requests.put(url).content))

    def post(self):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (jsonify(requests.replace(url).content))

class Game(Resource):
    def get(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (json.loads(requests.get(url).content))

    def delete(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (json.loads(requests.delete(url).content))

    def put(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (jsonify(requests.put(url).content))

    def post(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (jsonify(requests.replace(url).content))


class PlayTurn(Resource):
    def get(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (json.loads(requests.get(url).content))

    def delete(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (json.loads(requests.delete(url).content))

    def put(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (jsonify(requests.put(url).content))

    def post(self, id):
        url = request.base_url.replace('5000', '4000')
        print("url:", url)
        return (jsonify(requests.replace(url).content))

##
## Actually setup the Api resource routing here
##
api.add_resource(Games, '/games/')

api.add_resource(Game, '/games/<int:id>/')

api.add_resource(PlayTurn, '/games/<int:id>/play_turn')

# http://localhost:4000/games/32/play_turn/

if __name__ == '__main__':
    app.run(host='0.0.0.0')