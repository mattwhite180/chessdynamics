# # https://flask-restful.readthedocs.io/en/latest/quickstart.html
# # https://www.tutorialspoint.com/python_network_programming/python_http_client.htm

import os
import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)

def cleanUrl(url):
    newUrl = 'http://localhost:4000/' + url
    print("url: " + newUrl)
    return newUrl


class RESTapp(Resource):

    @staticmethod
    def get(path=''):  # <-- You should provide the default here not in api.add_resource()!
        url = cleanUrl(path)
        newpid = os.fork()
        if newpid == 0:
            return { "message": "hit " + url }
        else:
            requests.get(url)

api.add_resource(RESTapp, '/', '/<path:path>')  # Here just the URLs must be the arguments!


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# import requests
# from flask import Flask, request, jsonify, make_response
# from flask_restful import reqparse, abort, Api, Resource
# import json

# app = Flask(__name__)
# api = Api(app)

# parser = reqparse.RequestParser()
# parser.add_argument('task')

#     # some_json=request.get_json()
#     # return jsonify({'you sent ':some_json})

# # Game
# # shows a single game item and lets you delete a game item
# # class Games(Resource):
# #     def get(self):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (json.loads(requests.get(url).content))

# #     def delete(self):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (json.loads(requests.delete(url).content))

# #     def put(self):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (jsonify(requests.put(url).content))

# #     def post(self):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (jsonify(requests.replace(url).content))

# # class Game(Resource):
# #     def get(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (json.loads(requests.get(url).content))

# #     def delete(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (json.loads(requests.delete(url).content))

# #     def put(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (jsonify(requests.put(url).content))

# #     def post(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (jsonify(requests.replace(url).content))


# # class PlayTurn(Resource):
# #     def get(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (json.loads(requests.get(url).content))

# #     def delete(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (json.loads(requests.delete(url).content))

# #     def put(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (jsonify(requests.put(url).content))

# #     def post(self, id):
# #         url = request.base_url.replace('5000', '4000')
# #         print("url:", url)
# #         return (jsonify(requests.replace(url).content))

# class Endpoint(Resource):
#     def get(self):
#         url = cleanUrl(request.base_url)
#         print("url:", url)
#         return (json.loads(requests.get(url).content))

#     def delete(self):
#         url = cleanUrl(request.base_url)
#         print("url:", url)
#         return (json.loads(requests.delete(url).content))

#     def put(self):
#         url = cleanUrl(request.base_url)
#         print("url:", url)
#         return (jsonify(requests.put(url).content))

#     def post(self):
#         url = cleanUrl(request.base_url)
#         print("url:", url)
#         return (jsonify(requests.replace(url).content))


# # url = 'http://172.20.0.9:5000/games/'
# # listUrl = url.split(sep='5000')
# # listUrl
# # newUrl = 'http://localhost:4000' + listUrl[1]


# ##
# ## Actually setup the Api resource routing here
# ##
# # api.add_resource(Games, '/games/')

# # api.add_resource(Game, '/games/<int:id>/')

# # api.add_resource(PlayTurn, '/games/<int:id>/play_turn')

# api.add_resource(Endpoint, '/<path:content>')

# # http://localhost:4000/games/32/play_turn/

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')