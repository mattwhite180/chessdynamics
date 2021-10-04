from django.test import TestCase
from .models import Game
from .chessdynamics import ChessGame, GameHandler, Stockfish, Leela, RandomEngine
from django.utils import timezone
import chess
import chess.engine
import chess.pgn
import collections
import asyncio
import io


class ChessGameTestCase(TestCase):
    def setup(self):
        pass

    def test_load_game_parameters(self):
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        g = ChessGame("stockfish", "leela", moves)
        val = g.get_moves()
        expected = moves
        errmsg = "expected either " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_load_game_method(self):
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        g = ChessGame()
        g.load_game(moves)
        val = g.get_moves()
        expected = moves
        errmsg = "expected either " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_get_pgn_one(self):
        g = ChessGame("stockfish", "stockfish", "e2e3,e7e6,e1e2,e8e7", "chessdynamics")
        val = g.get_PGN()
        expected = (
            '[Event "chessdynamics"]\n'
            + '[Site "https://github.com/mattwhite180/chessdynamics"]\n'
            + '[Date "' + str(timezone.now().date()) + '"]\n'
            + '[Round "?"]\n'
            + '[White "stockfish"]\n'
            + '[Black "stockfish"]\n'
            + '[Result "*"]\n'
            + "\n"
            + "1. e3 e6 2. Ke2 Ke7 *"
        )
        errmsg = "expected either " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_get_pgn_two(self):
        g = ChessGame("stockfish", "stockfish")
        g.load_game("e2e3,e7e6,e1e2,e8e7")
        val = g.get_PGN()
        expected = (
            '[Event "undefined game"]\n'
            + '[Site "https://github.com/mattwhite180/chessdynamics"]\n'
            + '[Date "' + str(timezone.now().date()) + '"]\n'
            + '[Round "?"]\n'
            + '[White "stockfish"]\n'
            + '[Black "stockfish"]\n'
            + '[Result "*"]\n'
            + "\n"
            + "1. e3 e6 2. Ke2 Ke7 *"
        )
        errmsg = "expected either " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)


class GameHandlerTestCase(TestCase):
    def setUp(self):
        Game.objects.create(
            name="simple",
            description="test",
            move_list="",
            black="stockfish",
            white="stockfish",
            time_controls=100,
        )
        Game.objects.create(
            name="blackwins",
            description="test",
            move_list="",
            black="stockfish",
            white="stockfish",
            time_controls=100,
        )
        Game.objects.create(
            name="whitewins",
            description="test",
            move_list="",
            black="stockfish",
            white="stockfish",
            time_controls=100,
        )
        Game.objects.create(
            name="random",
            description="random vs lvl 1",
            move_list="",
            black="stockfish",
            white="random",
            time_controls=100,
        )

        Game.objects.create(
            name="leela",
            description="leela vs lvl 1",
            move_list="",
            black="leela",
            white="stockfish",
            time_controls=200,
        )

    def test_get_pgn_one_gm(self):
        g = Game.objects.get(name="simple")
        gm = GameHandler(g)
        gm.load_game("e2e3,e7e6,e1e2,e8e7")
        val = gm.get_PGN()
        expected = (
            '[Event "simple"]\n'
            + '[Site "https://github.com/mattwhite180/chessdynamics"]\n'
            + '[Date "' + str(timezone.now().date()) + '"]\n'
            + '[Round "?"]\n'
            + '[White "stockfish"]\n'
            + '[Black "stockfish"]\n'
            + '[Result "*"]\n'
            + "\n"
            + "1. e3 e6 2. Ke2 Ke7 *"
        )
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_fen_before_loading_game(self):
        g = Game.objects.get(name="simple")
        gm = GameHandler(g)
        val = gm.get_fen()
        expected = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        errmsg = "expected:\n" + str(expected) + "\nactual value was\n" + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_fen_after_loading_game(self):
        g = Game.objects.get(name="simple")
        gm = GameHandler(g)
        gm.load_game("e2e3,e7e6,e1e2,e8e7")
        val = gm.get_fen()
        expected = "rnbq1bnr/ppppkppp/4p3/8/8/4P3/PPPPKPPP/RNBQ1BNR w - - 2 3"
        errmsg = "expected:\n" + str(expected) + "\nactual value was\n" + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_play_move_good(self):
        g = Game.objects.get(name="simple")
        gm = GameHandler(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        gm.load_game(moves)
        val = gm.play_move("f3f7")
        expected = True
        errmsg = "expected " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_play_move_bad(self):
        g = Game.objects.get(name="simple")
        gm = GameHandler(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        gm.load_game(moves)
        val = gm.play_move("f3f8")
        expected = False
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_play_move_done(self):
        g = Game.objects.get(name="simple")
        gm = GameHandler(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,f3f7"
        gm.load_game(moves)
        val = gm.play_move("b4b3")
        expected = False
        errmsg = "expected " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_pop(self):
        g = Game.objects.get(name="simple")
        gm = GameHandler(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        gm.load_game(moves)
        gm.pop()
        val = gm.get_moves()
        expected = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)


class MachineTestCase(TestCase):
    def setup(self):
        pass

    def test_play_stockfish(self):
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        b = chess.Board()
        for i in moves.split(sep=","):
            b.push_uci(i)
        s = Stockfish(level=8, timeLimit=500)
        checkmates = ["f3f7", "c4f7"]
        actualMove = s.getMove(b)
        val = actualMove in checkmates
        expected = True
        errmsg = (
            "expected either " + str(checkmates) + " actual move was " + str(actualMove)
        )
        self.assertEqual(val, expected, errmsg)

    def test_play_leela(self):
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        b = chess.Board()
        for i in moves.split(sep=","):
            b.push_uci(i)
        l = Leela(timeLimit=500)
        checkmates = ["f3f7", "c4f7"]
        actualMove = l.getMove(b)
        val = actualMove in checkmates
        expected = True
        errmsg = (
            "expected either " + str(checkmates) + " actual move was " + str(actualMove)
        )
        self.assertEqual(val, expected, errmsg)
