import math
from utils import utility, terminal, result, actions, players, PLAYER_X


# Rule of play
# X always plays first


def min_value(board, alpha, beta):
    """
    Choose the action a in actions(s) that minimizes max - value(result(s, a))
    """

    #     beta = min(beta, v)
    #
    #     if alpha >= beta:
    #         break

    raise Exception("Not implemented yet")


def max_value(board, alpha, beta):
    """
    Choose the action a in actions(s) that maximizes min - value(result(s, a))
    """

    # alpha = max(alpha, v)
    #
    # if alpha >= beta:
    #     break

    raise Exception("Not implemented yet")


def ai_play(board):
    # alpha = -math.inf
    # beta = math.inf

    # if ai_mark == PLAYER_X:
    # val = min_value(result(board, action), alpha, beta)
    # alpha = max(alpha, val)

    # else:
    # val = max_value(result(board, action), alpha, beta)
    # beta = min(beta, val)

    raise Exception("Not implemented yet")
