from mydb import MyDB
from models import Game
from serializer import GameSerializer


def serialize_game(game_id):
    game_serial = GameSerializer(Game.objects.get(id=game_id))
    game = dict(game_serial.data)
    return game

    db = MyDB("games", "us-west-2")
    gs = serialize_game(5)
    db.upload(gs)
