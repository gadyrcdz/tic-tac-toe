import math
from utils import utility, terminal, result, actions, players, PLAYER_X


# Rule of play
# X always plays first


def min_value(board):
    """
    Choose the action a in actions(s) that minimizes max - value(result(s, a))
    """
    if(terminal(board)):
        return utility(board)

    v = math.inf

    for action in actions(board):
        resul = result(board, action)
        v = min(v, max_value(resul))

    return v


def max_value(board):
    """
    Choose the action a in actions(s) that maximizes min - value(result(s, a))
    """

    if(terminal(board)):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        resul = result(board,action)
        v = max(v, min_value(resul))
    return v



def ai_play(board):
    best_action = None
    ai_mark = players(board)

    if ai_mark == PLAYER_X:
        v = -math.inf

        for action in actions(board):
            val = min_value(result(board, action))
            if val > v:
                v = val
                best_action = action
    else:
        v = math.inf

        for action in actions(board):
            val = max_value(result(board, action))
            if val < v:
                v = val
                best_action = action

    return best_action
