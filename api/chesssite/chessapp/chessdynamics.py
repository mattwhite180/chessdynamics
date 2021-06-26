import chess
import chess.engine
import chess.pgn
import collections
import asyncio
import io

CHESS_CPU = {"stockfish": "/usr/games/stockfish"}


class ChessPlayer:
    def __init__(self, playerName="stockfish", timeLimitms=100, level=1, timeout=None):
        self.playerName = playerName.lower()
        self.timeLimit = float(timeLimitms) / 1000
        self.level = int(level)
        self.timeout = timeout
        self.engine = False
        self.isEngine = False

        if self.playerName in CHESS_CPU:
            self.isEngine = True
            self.engine = chess.engine.SimpleEngine.popen_uci(
                CHESS_CPU[self.playerName], timeout=self.timeout
            )
            self.engine.configure({"Skill Level": self.level})

    def is_cpu(self):
        return self.isEngine

    def __del__(self):
        if self.isEngine:
            self.engine.quit()

    def configure(self, d):
        if self.playerName != "human":
            self.engine.configure(d)

    def play(self, chessBoard):
        return self.engine.play(chessBoard, chess.engine.Limit(time=self.timeLimit))

    def get_player(self):
        return self.playerName

    def get_level(self):
        return self.level

    def get_timeout(self):
        return self.timeout

    def get_time_limit(self):
        return self.timeLimit


class ChessGame:
    def __init__(self, p1, p2, moves="", title="chessdynamics"):
        self.board = chess.Board()
        self.moves = moves
        self.game = chess.pgn.Game()
        self.node = self.game
        self.white = p1
        self.black = p2
        self.title = title
        self.load_game(moves)

    def load_game(self, moves):
        if len(moves) > 0:
            self.board = chess.Board()
            self.moves = moves
            for i in moves.split(sep=","):
                self.board.push(chess.Move.from_uci(i))
                self.node = self.node.add_variation(chess.Move.from_uci(i))

    def get_moves(self):
        return self.moves

    def print_game(self):
        return str(self.board)

    def is_game_over(self):
        return self.board.is_game_over()

    def get_legal_moves(self):
        moveStr = str()
        for i in self.board.legal_moves:
            if len(moveStr) == 0:
                moveStr += str(i)
            else:
                moveStr += "," + str(i)
        return moveStr

    def get_fen(self):
        return self.board.fen()

    def play_turn(self):
        if not self.is_game_over():
            if self.board.turn:
                result = self.white.play(self.board)
            else:
                result = self.black.play(self.board)
            self.node = self.node.add_variation(result.move)
            self.board.push(result.move)
            if len(self.moves) > 0:
                self.moves += "," + str(result.move)
            else:
                self.moves += str(result.move)
            return result
        else:
            return "gg"

    def play_continuous(self):
        while not self.is_game_over():
            self.play_turn()

    def get_PGN(self):
        self.set_headers()
        return str(self.game)

    def get_results(self):
        return self.board.result()

    def set_headers(self):
        self.game.headers["Event"] = self.title
        if self.white.get_player() not in CHESS_CPU:
            self.game.headers["White"] = self.white.get_player()
        else:
            self.game.headers["White"] = (
                self.white.get_player() + ":" + str(self.white.get_level())
            )
        if self.black.get_player() not in CHESS_CPU:
            self.game.headers["Black"] = self.black.get_player()
        else:
            self.game.headers["Black"] = (
                self.black.get_player() + ":" + str(self.black.get_level())
            )
        self.game.headers["Result"] = self.board.result()
        self.game.headers["Site"] = "ChessDynamics"


class GameModel:
    def __init__(self, gm):
        self.game_model = gm
        g = self.setup_game()
        self.save(g)

    def setup_white(self):
        return ChessPlayer(
            self.game_model.white,
            self.game_model.time_controls,
            self.game_model.white_level,
        )

    def setup_black(self):
        return ChessPlayer(
            self.game_model.black,
            self.game_model.time_controls,
            self.game_model.black_level,
        )

    def setup_game(self):
        w = self.setup_white()
        b = self.setup_black()
        cg = ChessGame(w, b, "", self.game_model.title)
        if len(self.game_model.move_list) > 0:
            cg.load_game(self.game_model.move_list)
        return cg

    def __str__(self):
        return self.setup_game().get_PGN()

    def get_moves(self):
        return self.setup_game().get_moves()

    def load_game(self, moveList):
        g = self.setup_game()
        g.load_game(moveList)
        self.save(g)

    def is_game_over(self):
        return self.setup_game().is_game_over()

    def get_results(self):
        return self.setup_game().get_results()

    def play_turn(self):
        g = self.setup_game()
        move = g.play_turn()
        self.save(g)
        return str(move.move)

    def play_continuous(self):
        g = self.setup_game()
        while not g.is_game_over():
            move = g.play_turn()
            self.save(g)
        return self.game_model.move_list

    def save(self, g):
        self.game_model.move_list = g.get_moves()
        self.game_model.results = g.get_results()
        self.game_model.fen = g.get_fen()
        self.game_model.legal_moves = g.get_legal_moves()
        self.game_model.save()

    def get_legal_moves(self):
        return self.setup_game().get_legal_moves()

    def get_fen(self):
        return self.setup_game().get_fen()

    def get_PGN(self):
        return self.setup_game().get_PGN()

    def print_game(self):
        return self.setup_game().print_game()

    def get_white_player(self):
        return self.setup_white().get_player()

    def get_black_player(self):
        return self.setup_black().get_player()

    def get_white_level(self):
        return self.setup_white().get_level()

    def get_black_level(self):
        return self.setup_black().get_level()
