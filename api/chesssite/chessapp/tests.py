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
        for i in moves.split(sep=","):
            b.push_uci(i)
        p = ChessPlayer("stockfish", 123, 7, None)
        checkmates = ["f3f7", "c4f7"]
        actualMove = p.play(b)
        val = actualMove in checkmates
        expected = True
        errmsg = (
            "expected either " + str(checkmates) + " actual move was " + str(actualMove)
        )
        self.assertEqual(val, expected, errmsg)

    def test_cpu_name(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.is_cpu()
        expected = True
        errmsg = (
            "expected value for ChessPlayer.is_cpu() is "
            + str(expected)
            + " actual value is "
            + str(val)
        )
        self.assertEqual(val, expected, errmsg)

    def test_human_name(self):
        p = ChessPlayer("matthew", 123, 7, None)
        val = p.is_cpu()
        expected = False
        errmsg = (
            "expected value for ChessPlayer.is_cpu() is "
            + str(expected)
            + " actual value is "
            + str(val)
        )
        self.assertEqual(val, expected, errmsg)

    def test_get_level(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.get_level()
        expected = 7
        errmsg = (
            "expected value from p.get_level() is "
            + str(expected)
            + " actual value was "
            + str(val)
        )
        self.assertEqual(val, expected, errmsg)

    def test_get_timeout(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.get_timeout()
        expected = None
        errmsg = (
            "expected value from p.get_timeout() is "
            + str(expected)
            + " actual value was "
            + str(val)
        )
        self.assertEqual(val, expected, errmsg)

    def test_get_time_limit(self):
        p = ChessPlayer("stockfish", 123, 7, None)
        val = p.get_time_limit()
        expected = 123 / 1000
        errmsg = (
            "expected value for ChessPlayer.get_time_limit() is "
            + str(expected)
            + " actual value is "
            + str(val)
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
        errmsg = "expected either " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_load_game_method(self):
        w = ChessPlayer("stockfish", 123, 1, None)
        b = ChessPlayer("stockfish", 123, 8, None)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        g = ChessGame(w, b)
        g.load_game(moves)
        val = g.get_moves()
        expected = moves
        errmsg = "expected either " + str(expected) + " actual value was " + str(val)
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
            "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,c4f7",
        ]
        actualMove = g.get_moves()
        val = actualMove in checkmates
        expected = True
        errmsg = (
            "expected either " + str(checkmates) + " actual move was " + str(actualMove)
        )
        self.assertEqual(val, expected, errmsg)

    def test_full_game_black_wins(self):
        w = ChessPlayer("stockfish", 100, 1, None)
        b = ChessPlayer("stockfish", 100, 8, None)
        g = ChessGame(w, b)
        g.play_continuous()
        val = g.get_results()
        expected = "0-1"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_full_game_white_wins(self):
        w = ChessPlayer("stockfish", 100, 8, None)
        b = ChessPlayer("stockfish", 100, 1, None)
        g = ChessGame(w, b)
        g.play_continuous()
        val = g.get_results()
        expected = "1-0"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_full_game_manual(self):
        w = ChessPlayer("stockfish", 100, 1, None)
        b = ChessPlayer("stockfish", 100, 8, None)
        g = ChessGame(w, b)
        while not g.is_game_over():
            g.play_turn()
        val = g.get_results()
        expected = "0-1"
        errmsg = "expected either " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_get_pgn_one(self):
        w = ChessPlayer("stockfish", 100, 1, None)
        b = ChessPlayer("stockfish", 100, 8, None)
        g = ChessGame(w, b, "e2e3,e7e6,e1e2,e8e7")
        val = g.get_PGN()
        expected = (
            '[Event "chessdynamics"]\n'
            + '[Site "ChessDynamics"]\n'
            + '[Date "????.??.??"]\n'
            + '[Round "?"]\n'
            + '[White "stockfish:1"]\n'
            + '[Black "stockfish:8"]\n'
            + '[Result "*"]\n'
            + "\n"
            + "1. e3 e6 2. Ke2 Ke7 *"
        )
        errmsg = "expected either " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_get_pgn_two(self):
        w = ChessPlayer("stockfish", 100, 1, None)
        b = ChessPlayer("stockfish", 100, 8, None)
        g = ChessGame(w, b)
        g.load_game("e2e3,e7e6,e1e2,e8e7")
        val = g.get_PGN()
        expected = (
            '[Event "chessdynamics"]\n'
            + '[Site "ChessDynamics"]\n'
            + '[Date "????.??.??"]\n'
            + '[Round "?"]\n'
            + '[White "stockfish:1"]\n'
            + '[Black "stockfish:8"]\n'
            + '[Result "*"]\n'
            + "\n"
            + "1. e3 e6 2. Ke2 Ke7 *"
        )
        errmsg = "expected either " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_turn_white(self):
        w = ChessPlayer("stockfish", 123, 1, None)
        b = ChessPlayer("stockfish", 123, 8, None)
        g = ChessGame(w, b)
        val = g.get_turn()
        expected = "white"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_turn_black(self):
        w = ChessPlayer("stockfish", 123, 1, None)
        b = ChessPlayer("stockfish", 123, 8, None)
        g = ChessGame(w, b, "e2e3")
        val = g.get_turn()
        expected = "black"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)


class GameModelTestCase(TestCase):
    def setUp(self):
        Game.objects.create(
            name="simple",
            description="test",
            move_list="",
            black="stockfish",
            black_level=8,
            white="stockfish",
            white_level=1,
            time_controls=100,
        )
        Game.objects.create(
            name="blackwins",
            description="test",
            move_list="",
            black="stockfish",
            black_level=8,
            white="stockfish",
            white_level=1,
            time_controls=100,
        )
        Game.objects.create(
            name="whitewins",
            description="test",
            move_list="",
            black="stockfish",
            black_level=1,
            white="stockfish",
            white_level=8,
            time_controls=100,
        )
        Game.objects.create(
            name="random",
            description="random vs lvl 1",
            move_list="",
            black="stockfish",
            black_level=8,
            white="random",
            white_level=2,
            time_controls=100,
        )

        Game.objects.create(
            name="leela",
            description="leela vs lvl 1",
            move_list="",
            black="leela",
            black_level=1,
            white="stockfish",
            white_level=1,
            time_controls=200,
        )

    def test_easy_checkmate_gm(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        gm.load_game(moves)
        gm.play_turn()
        checkmates = [
            "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,f3f7",
            "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,c4f7",
        ]
        actualMove = gm.get_moves()
        val = actualMove in checkmates
        expected = True
        errmsg = (
            "expected either " + str(checkmates) + " actual move was " + str(actualMove)
        )
        self.assertEqual(val, expected, errmsg)

    def test_full_game_black_wins_gm(self):
        g = Game.objects.get(name="blackwins")
        gm = GameModel(g)
        gm.play_continuous()
        val = gm.get_results()
        expected = "0-1"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_full_game_white_wins_gm(self):
        g = Game.objects.get(name="whitewins")
        gm = GameModel(g)
        gm.play_continuous()
        val = gm.get_results()
        expected = "1-0"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_full_game_manual_gm(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        while not gm.is_game_over():
            gm.play_turn()
        val = gm.get_results()
        expected = "0-1"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_get_pgn_one_gm(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        gm.load_game("e2e3,e7e6,e1e2,e8e7")
        val = gm.get_PGN()
        expected = (
            '[Event "simple"]\n'
            + '[Site "ChessDynamics"]\n'
            + '[Date "????.??.??"]\n'
            + '[Round "?"]\n'
            + '[White "stockfish:1"]\n'
            + '[Black "stockfish:8"]\n'
            + '[Result "*"]\n'
            + "\n"
            + "1. e3 e6 2. Ke2 Ke7 *"
        )
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_fen_before_loading_game(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        val = gm.get_fen()
        expected = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        errmsg = "expected:\n" + str(expected) + "\nactual value was\n" + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_fen_after_loading_game(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        gm.load_game("e2e3,e7e6,e1e2,e8e7")
        val = gm.get_fen()
        expected = "rnbq1bnr/ppppkppp/4p3/8/8/4P3/PPPPKPPP/RNBQ1BNR w - - 2 3"
        errmsg = "expected:\n" + str(expected) + "\nactual value was\n" + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_fen_after_playing_game(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        moves = "e2e3,e7e6,e1e2,e8e7"
        for i in moves.split(sep=","):
            gm.play_move(i)
        val = gm.get_fen()
        expected = "rnbq1bnr/ppppkppp/4p3/8/8/4P3/PPPPKPPP/RNBQ1BNR w - - 2 3"
        errmsg = "expected:\n" + str(expected) + "\nactual value was\n" + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_play_move_good(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        gm.load_game(moves)
        val = gm.play_move("f3f7")
        expected = True
        errmsg = "expected " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_play_move_bad(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        gm.load_game(moves)
        val = gm.play_move("f3f8")
        expected = False
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_play_move_done(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3,f3f7"
        gm.load_game(moves)
        val = gm.play_move("b4b3")
        expected = False
        errmsg = "expected " + str(expected) + " actual move was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_full_game_black_wins_random_gm(self):
        g = Game.objects.get(name="random")
        gm = GameModel(g)
        gm.play_continuous()
        val = gm.get_results()
        expected = "0-1"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_full_game_black_wins_leela_gm(self):
        g = Game.objects.get(name="leela")
        gm = GameModel(g)
        gm.play_continuous()
        val = gm.get_results()
        expected = "0-1"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)

    def test_pop(self):
        g = Game.objects.get(name="simple")
        gm = GameModel(g)
        moves = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4,a4a3"
        gm.load_game(moves)
        gm.pop()
        val = gm.get_moves()
        expected = "e2e4,a7a6,d1f3,a6a5,f1d3,a5a4,d3c4"
        errmsg = "expected " + str(expected) + " actual value was " + str(val)
        self.assertEqual(val, expected, errmsg)
