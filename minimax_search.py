import math
import numpy as np
import connect_four
import hashlib
import sys
sys.path.append(".\\")
print(sys.path)
from evaluation_utils import *

MIN = -1
MAX = 1

CACHE = {}

class StateSpace:
    def __init__(self, game):
        self.game = game

    def successors(self, player):
        successors = []

        for column in range(self.game.cols):
            successor_board, last_move = self.game.simulate_insert(column, player)

            if not np.array_equal(self.game.board, successor_board):
                successor = StateSpace(connect_four.Game(self.game.cols, self.game.rows, self.game.win, self.game.move_list + str(player) + str(column), last_move))
                successor.game.board = successor_board
                successors.append(successor)

        return successors


def search(state, player, alpha=-math.inf, beta=math.inf, max_depth = 6):
    md5 = hashlib.md5(state.game.move_list.encode('utf-8'))

    cache_result = CACHE.get(state.game.move_list.encode('utf-8'))
    if cache_result is not None:
        if cache_result != connect_four.NOT_OVER:
            return cache_result, None
    else:
        check_game_over = state.game.checkForWin()
        CACHE[state.game.move_list.encode('utf-8')] = check_game_over

        if check_game_over != connect_four.NOT_OVER:
            return check_game_over, None

    if max_depth == 0:
        ret_val = evaluate_based_on_location_ratings(state)
        return ret_val, None

    if player == MIN:
        min_state = None
        min_value = math.inf
        for state in state.successors(player):
            a,b = search(state, MAX, alpha, beta, max_depth - 1)

            if a <= alpha:
                # print("Pruned")
                return a, state

            beta = min(beta, a)

            if a < min_value:
                min_value = a
                min_state = state

        # print("Min player returned min_state")
        return min_value, min_state
    else:
        max_state = None
        max_value = - math.inf
        for state in state.successors(player):
            a,b = search(state, MIN, alpha, beta, max_depth - 1)

            if a >= beta:
                # print("Pruned")
                return a, state

            alpha = max(alpha, a)

            if a > max_value:
                max_value = a
                max_state = state

        # print("Max player returned max_state")
        return max_value, max_state


