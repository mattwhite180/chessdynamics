import chess
import chess.engine
import chess.pgn
import collections
import asyncio
import io

def playOneCPU(player, level, limit):
    pass


def playTwoCPU(playerOne, playerTwo, levelOne, levelTwo, timeLimit):
    levelOne = int(levelOne)
    levelTwo = int(levelTwo)
    timeLimit = float(timeLimit) / 1000
    print("playerOne:", playerOne, type(playerOne))
    print("playerTwo:", playerTwo, type(playerTwo))
    print("levelOne:", levelOne, type(levelOne))
    print("levelTwo:", levelTwo, type(levelTwo))
    print("timeLimit:", timeLimit, type(timeLimit))
    engineOne = chess.engine.SimpleEngine.popen_uci(
        "/usr/games/stockfish", timeout=None
    )
    engineOne.configure({"Skill Level": levelOne})
    engineTwo = chess.engine.SimpleEngine.popen_uci(
        "/usr/games/stockfish", timeout=None
    )
    engineTwo.configure({"Skill Level": levelTwo})
    game = chess.pgn.Game()
    node = game
    game.headers["Event"] = "Example"
    game.headers["White"] = str(levelOne)
    game.headers["Black"] = str(levelTwo)
    turn = False
    board = chess.Board()
    while not board.is_game_over():
        if turn:
            result = engineOne.play(board, chess.engine.Limit(time=timeLimit))
        else:
            result = engineTwo.play(board, chess.engine.Limit(time=timeLimit))
        node = node.add_variation(result.move)
        turn = not turn
        board.push(result.move)
        print(result.move)

    engineOne.quit()
    engineTwo.quit()
    game.headers["Result"] = board.result()
    game.headers["Site"] = "ChessDynamics"
    game.headers["Round"] = str(timeLimit) + " ms"
    return str(game)
