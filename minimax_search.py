import math
import numpy as np
import connect_four

MIN = -1
MAX = 1

class StateSpace:
    def __init__(self, game):
        self.game = game

    def successors(self, player):
        successors = []

        for successor_board in self.game.generate_successors(player):
            successor = StateSpace(connect_four.Game(self.game.cols, self.game.rows, self.game.win))
            successor.game.board = successor_board
            successors.append(successor)

        return successors


def search(state, player, max_depth = 4):
    # print("Call to search")
    check_game_over = connect_four.check_for_win(state.game)

    if check_game_over is not None:
        # print("Check game over")
        # print(check_game_over)
        return check_game_over, None

    elif max_depth == 0:
        # print("MAx depth")
        ret_val = evaluation_function(state)
        # print(str(ret_val))
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
