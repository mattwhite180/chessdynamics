import chess
import chess.engine
import chess.pgn
import collections
from random import randrange
from django.utils import timezone
import io


class Stockfish:
    def __init__(self, level=1, timeLimit=1000):
        if timeLimit < 250:
            timeLimit = 250
        self.url = "/root/stockfish/stockfish_14_linux_x64/stockfish_14_x64"
        self.engine = chess.engine.SimpleEngine.popen_uci(self.url, timeout=None)
        self.skillLevel = level
        self.setSkillLevel(level)
        self.setTimeLimit(timeLimit)

    def __del__(self):
        self.engine.quit()

    def getMove(self, chessBoard):
        return str(
            self.engine.play(chessBoard, chess.engine.Limit(time=self.timeLimit)).move
        )

    def setSkillLevel(self, level):
        self.skillLevel = level
        self.engine.configure({"Skill Level": int(level)})

    def setTimeLimit(self, tl):
        self.timeLimit = tl / 1000

    def getSkillLevel(self):
        return self.skillLevel

    def getTimeLimit(self):
        return self.timeLimit


class Leela:
    def __init__(self, timeLimit=1000):
        if timeLimit < 250:
            timeLimit = 250
        self.url = "/root/stockfish/stockfish_14_linux_x64/stockfish_14_x64"
        self.engine = chess.engine.SimpleEngine.popen_uci(self.url, timeout=None)
        self.setTimeLimit(timeLimit)

    def __del__(self):
        self.engine.quit()

    def getMove(self, chessBoard):
        return str(
            self.engine.play(chessBoard, chess.engine.Limit(time=self.timeLimit)).move
        )

    def setTimeLimit(self, tl):
        self.timeLimit = tl / 1000

    def getTimeLimit(self):
        return self.timeLimit


class RandomEngine:
    def __init__(self):
        pass

    def getMove(self, chessBoard):
        legalMoves = list()
        for i in chessBoard.legal_moves:
            legalMoves.append(str(i))
        return legalMoves[randrange(len(legalMoves))]


class ChessGame:
    def __init__(
        self, p1="undefined p1", p2="undefined p2", moves="", name="undefined game"
    ):
        self.board = chess.Board()
        self.moves = moves
        self.game = chess.pgn.Game()
        self.node = self.game
        self.white = p1
        self.black = p2
        self.name = name
        self.load_game(moves)

    def load_game(self, moves):
        if len(moves) > 0:
            self.board = chess.Board()
            self.moves = moves
            self.game = chess.pgn.Game()
            self.node = self.game
            for i in moves.split(sep=","):
                self.board.push(chess.Move.from_uci(i))
                self.node = self.node.add_variation(chess.Move.from_uci(i))

    def get_moves(self):
        return self.moves

    def get_board(self):
        return self.board

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

    def get_turn(self):
        if self.board.turn:
            return "white"
        else:
            return "black"

    def play_move(self, move):
        if self.is_game_over():
            return False
        elif move not in self.get_legal_moves().split(sep=","):
            return False
        else:
            self.board.push_uci(move)
            self.node = self.node.add_variation(chess.Move.from_uci(move))
            if len(self.moves) > 0:
                self.moves += "," + str(move)
            else:
                self.moves += str(move)
            return True

    def get_PGN(self, date = timezone.now()):
        self.set_headers(date)
        return str(self.game)

    def get_results(self):
        return self.board.result()

    def set_headers(self, date = timezone.now()):
        self.game.headers["Event"] = self.name
        self.game.headers["White"] = self.white
        self.game.headers["Black"] = self.black
        self.game.headers["Result"] = self.board.result()
        self.game.headers["Date"] = date.date()
        self.game.headers["Site"] = "https://github.com/mattwhite180/chessdynamics"


class GameHandler:
    def __init__(self, gm):
        self.game_model = gm
        if self.game_model.available:
            self.game_model.available = False
            self.game_model.save()
            self.available = True
        else:
            self.available = False
        self.game_model.save()
        self.deleted = False
        g = self.setup_game()
        self.save(g)

    def __del__(self):
        if self.deleted:
            self.game_model.delete()
        elif self.available:
            self.game_model.available = True
        self.game_model.save()

    def delete(self):
        self.deleted = True

    def setup_game(self):
        w = self.game_model.white
        b = self.game_model.black
        cg = ChessGame(w, b, "", self.game_model.name)
        if len(self.game_model.move_list) > 0:
            cg.load_game(self.game_model.move_list)
        return cg

    def __str__(self):
        return self.setup_game().get_PGN()

    def get_board(self):
        return self.setup_game().get_board()

    def get_moves(self):
        return self.setup_game().get_moves()

    def load_game(self, moveList):
        if self.available:
            g = self.setup_game()
            g.load_game(moveList)
            self.save(g)
            return "loaded game"
        else:
            return "game is marked 'unavailable'"

    def is_game_over(self):
        return self.setup_game().is_game_over()

    def get_results(self):
        return self.setup_game().get_results()

    def play_move(self, move):
        if self.available:
            g = self.setup_game()
            val = g.play_move(move)
            self.save(g)
            return val
        else:
            return "game is marked 'unavailable'"

    def get_turn(self):
        return self.setup_game().get_turn()

    def pop(self):
        if self.available:
            g = self.setup_game()
            if len(g.get_moves()) == 0:
                return True
            elif g.get_moves().count(",") == 0:
                move = g.get_moves().replace(",", "")
                self.game_model.move_list = ""
                self.game_model.save()
                g = self.setup_game()
                self.save(g)
                return move
            elif g.get_moves().count(",") > 0:
                # moveList = g.get_moves().split(',')
                # move = str(moveList[-1])
                # newMoves = moveList[0]
                # for i in range(1, len(moveList) - 1):
                #     newMoves += "," + moveList[i]
                # g.load_game(newMoves)
                # self.save(g)
                # return move
                move = g.get_moves()[g.get_moves().rindex(",") :]
                g.load_game(g.get_moves()[0 : g.get_moves().rindex(",")])
                self.save(g)
                return str(move).replace(",", "")
            else:
                return str(False)
        return "game is marked 'unavailable'"

    def save(self, g):
        if self.available:
            self.game_model.turn = g.get_turn()
            self.game_model.move_list = g.get_moves()
            self.game_model.results = g.get_results()
            self.game_model.fen = g.get_fen()
            self.game_model.legal_moves = g.get_legal_moves()
            self.game_model.pgn = g.get_PGN(self.game_model.creation_date)
            self.game_model.save()

    def save_game(self):
        if self.available:
            self.game_model.save()
            self.save(self.setup_game())

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
