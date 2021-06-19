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

        if self.playerName not in CHESS_CPU:
            self.engine = False
            self.isEngine = False
        else:
            self.isEngine = True
            self.engine = chess.engine.SimpleEngine.popen_uci(
                CHESS_CPU[self.playerName], timeout=self.timeout
            )
            self.engine.configure({"Skill Level": self.level})

    def __del__(self):
        if self.isEngine:
            self.engine.quit()

    def getConfigure(self, d):
        if self.playerName != "human":
            self.engine.configure(d)

    def configure(self, val1, val2):
        self.engine.configure({val1: val2})

    def play(self, chessBoard):
        return self.engine.play(chessBoard, chess.engine.Limit(time=self.timeLimit))

    def getPlayer(self):
        return self.playerName

    def getLevel(self):
        return self.level

    def getTimeout(self):
        return self.timeout

    def getTimeLimit(self):
        return self.timeLimit


def playOneCPU(player, level, limit):
    pass


class ChessGame:
    def __init__(self, p1, p2, title="chessdynamics"):
        self.board = chess.Board()
        self.game = chess.pgn.Game()
        self.node = self.game
        self.white = p1
        self.black = p2
        self.whiteTurn = True
        self.title = title

    def is_game_over(self):
        return self.board.is_game_over()

    def play_turn(self):
        if not self.is_game_over():
            if self.whiteTurn:
                result = self.white.play(self.board)
            else:
                result = self.black.play(self.board)
            self.node = self.node.add_variation(result.move)
            self.whiteTurn = not self.whiteTurn
            self.board.push(result.move)
            return result.move
        else:
            return "gg"

    def play_continuous(self):
        while not self.is_game_over():
            self.play_turn()

    def get_PGN(self):
        self.set_headers()
        return str(self.game)

    def set_headers(self):
        self.game.headers["Event"] = self.title
        if self.white.getPlayer() not in CHESS_CPU:
            self.game.headers["White"] = self.white.getPlayer()
        else:
            self.game.headers["White"] = (
                self.white.getPlayer() + ":" + str(self.white.getLevel())
            )
        if self.black.getPlayer() not in CHESS_CPU:
            self.game.headers["Black"] = self.black.getPlayer()
        else:
            self.game.headers["Black"] = (
                self.black.getPlayer() + ":" + str(self.black.getLevel())
            )
        self.game.headers["Result"] = self.board.result()
        self.game.headers["Site"] = "ChessDynamics"
