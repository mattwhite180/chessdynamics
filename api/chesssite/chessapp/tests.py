from django.test import TestCase
from .models import Game
from .chessdynamics import ChessPlayer, ChessGame, GameModel 
import chess
import chess.engine
import chess.pgn
import collections
import asyncio
import io


class ChessPlayerTestCase(TestCase):
    def setup(self):
        pass

    def test_play_stockfish(self):
        g = chess.pgn.Game()
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        b = chess.Board()
        for i in moves.split(sep=','):
            b.push_uci(i)
        p = ChessPlayer("stockfish", 123, 7, None)
        checkmates = ["f3f7", "c4f7"]
        actualMove = str(p.play(b).move)
        val = actualMove in checkmates
        expected = True
        errmsg = (
            "expected either " + str(checkmates) +
            " actual move was " + str(actualMove)
        )
        self.assertEqual(val, expected, errmsg)

    def test_cpu_name(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.is_cpu()
        expected = True
        errmsg = (
            "expected value for ChessPlayer.is_cpu() is " + str(expected) +
            " actual value is " + str(val)
        )
        self.assertEqual(val, expected, errmsg) 

    def test_human_name(self):
        p = ChessPlayer("matthew", 123, 7, None)
        val = p.is_cpu()
        expected = False
        errmsg = (
            "expected value for ChessPlayer.is_cpu() is " + str(expected) +
            " actual value is " + str(val)
        )
        self.assertEqual(val, expected, errmsg)

    def test_get_level(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.get_level()
        expected = 7
        errmsg = (
            "expected value from p.get_level() is " + str(expected) +
            " actual value was " + str(val)
        )
        self.assertEqual(val, expected, errmsg)

    def test_get_timeout(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.get_timeout()
        expected = None
        errmsg = (
            "expected value from p.get_timeout() is " + str(expected) +
            " actual value was " + str(val)
        )
        self.assertEqual(val, expected, errmsg) 

    def test_get_time_limit(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.get_time_limit()
        expected = 123 / 1000
        errmsg = (
            "expected value for ChessPlayer.get_time_limit() is " + str(expected) +
            " actual value is " + str(val)
        )
        self.assertEqual(val, expected, errmsg)

class ChessGameTestCase(TestCase):
    def setup(self):
        pass

    def test_load_game_parameters(self):
        w = ChessPlayer("stockfish", 123, 1, None)
        b = ChessPlayer("stockfish", 123, 8, None)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        g = ChessGame(w, b, moves)
        val = g.get_moves()
        expected = moves
        errmsg = (
            "expected either " + str(val) +
            " actual value was " + str(expected)
        )
        self.assertEqual(val, expected, errmsg)


    def test_load_game_method(self):
        w = ChessPlayer("stockfish", 123, 1, None)
        b = ChessPlayer("stockfish", 123, 8, None)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        g = ChessGame(w, b)
        g.load_game(moves)
        val = g.get_moves()
        expected = moves
        errmsg = (
            "expected either " + str(val) +
            " actual value was " + str(expected)
        )
        self.assertEqual(val, expected, errmsg)

    def test_easy_checkmate(self):
        w = ChessPlayer("stockfish", 123, 1, None)
        b = ChessPlayer("stockfish", 123, 8, None)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        g = ChessGame(w, b)
        g.load_game(moves)
        g.play_turn()
        checkmates = [
            "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,f3f7",
            "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,c4f7"
            ]
        actualMove = g.get_moves()
        val = actualMove in checkmates
        expected = True
        errmsg = (
            "expected either " + str(checkmates) +
            " actual move was " + str(actualMove)
        )
        self.assertEqual(val, expected, errmsg)

    def test_full_game(self):
        w = ChessPlayer("stockfish", 10, 1, None)
        b = ChessPlayer("stockfish", 10, 8, None)
        g = ChessGame(w, b)
        g.play_continuous()
        val = g.get_results()
        expected = "0-1"
        errmsg = (
            "expected either " + str(val) +
            " actual value was " + str(expected)
        )
        self.assertEqual(val, expected, errmsg)

    def test_full_game_manual(self):
        w = ChessPlayer("stockfish", 10, 1, None)
        b = ChessPlayer("stockfish", 10, 8, None)
        g = ChessGame(w, b)
        while not g.is_game_over():
            g.play_turn()
        val = g.get_results()
        expected = "0-1"
        errmsg = (
            "expected either " + str(val) +
            " actual value was " + str(expected)
        )
        self.assertEqual(val, expected, errmsg)

    def test_get_pgn_one(self):
        w = ChessPlayer("stockfish", 10, 1, None)
        b = ChessPlayer("stockfish", 10, 8, None)
        g = ChessGame(w, b, "e2e3,e7e6,e1e2,e8e7")
        val = g.get_PGN()
        expected = ('[Event "chessdynamics"]\n' +
        '[Site "ChessDynamics"]\n' +
        '[Date "????.??.??"]\n' +
        '[Round "?"]\n' +
        '[White "stockfish:1"]\n' +
        '[Black "stockfish:8"]\n' +
        '[Result "*"]\n' +
        '\n' +
        '1. e3 e6 2. Ke2 Ke7 *')
        errmsg = (
            "expected either " + str(val) +
            " actual move was " + str(expected)
        )
        self.assertEqual(val, expected, errmsg)

    def test_get_pgn_two(self):
        w = ChessPlayer("stockfish", 10, 1, None)
        b = ChessPlayer("stockfish", 10, 8, None)
        g = ChessGame(w, b)
        g.load_game("e2e3,e7e6,e1e2,e8e7")
        val = g.get_PGN()
        expected = ('[Event "chessdynamics"]\n' +
        '[Site "ChessDynamics"]\n' +
        '[Date "????.??.??"]\n' +
        '[Round "?"]\n' +
        '[White "stockfish:1"]\n' +
        '[Black "stockfish:8"]\n' +
        '[Result "*"]\n' +
        '\n' +
        '1. e3 e6 2. Ke2 Ke7 *')
        errmsg = (
            "expected either " + str(val) +
            " actual move was " + str(expected)
        )
        self.assertEqual(val, expected, errmsg)


#Class BongCloudTestCase(TestCase):
