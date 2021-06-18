import chess
import chess.engine
import chess.pgn
import collections
import asyncio
import io

CHESS_CPU = {"stockfish": "/usr/games/stockfish"}


class ChessPlayer:
    def __init__(self, playerName="stockfish", timeLimit=100, level=1, timeout=None):
        self.playerName = playerName
        self.timeLimit = timeLimit
        self.level = level
        self.timeout = timeout

        if playerName.lower() == "human":
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


class ChessGame(p1, p2):

    def __init__(self):
        self.game = chess.pgn.Game()
        self.node = self.game

    def setHeaders(self):
        self.game.headers["Event"] = "Example"
        self.game.headers["White"] = str(whiteLevel)
        self.game.headers["Black"] = str(blackLevel)
        self.game.headers["Result"] = board.result()
        self.game.headers["Site"] = "ChessDynamics"
        self.game.headers["Round"] = str(timeLimit) + " ms"

def playTwoCPU(whitePlayer, blackPlayer, whiteLevel, blackLevel, timeLimit):
    whiteLevel = int(whiteLevel)
    blackLevel = int(blackLevel)
    timeLimit = float(timeLimit) / 1000
    # engineOne = chess.engine.SimpleEngine.popen_uci(
    #     "/usr/games/stockfish", timeout=None
    # )
    # engineOne.configure({"Skill Level": whiteLevel})
    # engineTwo = chess.engine.SimpleEngine.popen_uci(
    #     "/usr/games/stockfish", timeout=None
    # )
    # engineTwo.configure({"Skill Level": levelTwo})
    whiteEngine = ChessPlayer("stockfish", timeLimit, whiteLevel, None)
    blackEngine = ChessPlayer("stockfish", timeLimit, blackLevel, None)
    game = chess.pgn.Game()
    node = game
    game.headers["Event"] = "Example"
    game.headers["White"] = str(whiteLevel)
    game.headers["Black"] = str(blackLevel)
    turn = True
    board = chess.Board()
    while not board.is_game_over():
        if turn:
            result = whiteEngine.play(board)
        else:
            result = blackEngine.play(board)
        node = node.add_variation(result.move)
        turn = not turn
        board.push(result.move)
        print(result.move)
    game.headers["Result"] = board.result()
    game.headers["Site"] = "ChessDynamics"
    game.headers["Round"] = str(timeLimit) + " ms"
    return str(game)
