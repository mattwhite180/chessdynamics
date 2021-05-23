import chess
import chess.engine
import chess.pgn
import collections
import asyncio


def board_to_pgn(board):
    # from https://github.com/niklasf/python-chess/issues/63
    game = chess.pgn.Game()

    # Undo all moves.
    switchyard = collections.deque()
    while board.move_stack:
        switchyard.append(board.pop())

    game.setup(board)
    node = game

    # Replay all moves.
    while switchyard:
        move = switchyard.pop()
        node = node.add_variation(move)
        board.push(move)

    game.headers["Result"] = board.result()
    return str(game)

def playgame(playerOne, playerTwo, levelOne, levelTwo, timeLimit):
    levelOne = int(levelOne)
    levelTwo = int(levelTwo)
    timeLimit = float(timeLimit)
    print("playerOne:", playerOne, type(playerOne))
    print("playerTwo:", playerTwo, type(playerTwo))
    print("levelOne:", levelOne, type(levelOne))
    print("levelTwo:", levelTwo, type(levelTwo))
    print("timeLimit:", timeLimit, type(timeLimit))
    engineOne = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish", timeout=None)
    engineOne.configure({"Skill Level": levelOne})
    engineTwo = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish", timeout=None)
    engineTwo.configure({"Skill Level": levelTwo})
    game = chess.pgn.Game()
    game.headers["Event"] = "Example"
    turn = False
    board = chess.Board()
    while not board.is_game_over():
        if turn:
            result = engineOne.play(board, chess.engine.Limit(time=timeLimit))
        else:
            result = engineTwo.play(board, chess.engine.Limit(time=timeLimit))
        turn = not turn
        board.push(result.move)
        print()
        print(board)

    print(board)
    engineOne.quit()
    engineTwo.quit()
    return board

