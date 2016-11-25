import math
import numpy as np
import connect_four
import hashlib

MIN = -1
MAX = 1

CACHE = {}

class StateSpace:
    def __init__(self, game):
        self.game = game

    def successors(self, player):
        successors = []

        for column in range(self.game.cols):
            successor_board = self.game.simulate_insert(column, player)
            if not np.array_equal(self.game.board, successor_board):
                successor = StateSpace(connect_four.Game(self.game.cols, self.game.rows, self.game.win, self.game.move_list + str(player) + str(column)))
                successor.game.board = successor_board
                successors.append(successor)

        return successors


def search(state, player, max_depth = 4):
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
        ret_val = evaluation_function(state)
        return evaluation_function(state), None

    if player == MIN:
        min_state = None
        min_value = math.inf
        for state in state.successors(player):
            a,b = search(state, MAX, max_depth - 1)

            if a < min_value:
                min_value = a
                min_state = state

        # print("Min player returned min_state")
        return min_value, min_state
    else:
        max_state = None
        max_value = - math.inf
        for state in state.successors(player):
            a,b = search(state, MIN, max_depth - 1)

            if a > max_value:
                max_value = a
                max_state = state

        # print("Max player returned max_state")
        return max_value, max_state


def evaluation_function(state):
    return np.random.uniform(-1,1,1)[0]
