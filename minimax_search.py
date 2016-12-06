import math
import numpy as np
import connect_four
import hashlib
import sys
sys.path.append(".\\")
from evaluation_utils import *
import pickle
import operator

MIN = -1
MAX = 1

CACHE = {}

class StateSpace:
    def __init__(self, game, eval_func=evaluate_using_both):
        self.game = game
        self.eval_func = eval_func

    def successors(self, player):
        successors = []

        for column in range(self.game.cols):
            successor_board, last_move = self.game.simulate_insert(column, player)

            if not np.array_equal(self.game.board, successor_board):
                successor = StateSpace(connect_four.Game(self.game.cols, self.game.rows, self.game.win, self.game.move_list + str(player) + str(column), last_move), self.eval_func)
                successor.game.board = successor_board
                successors.append(successor)

        return successors

    def successorsSorted(self, player):
        successors = dict()

        for column in range(self.game.cols):
            successor_board, last_move = self.game.simulate_insert(column, player)

            if not np.array_equal(self.game.board, successor_board):
                successor = StateSpace(connect_four.Game(self.game.cols, self.game.rows, self.game.win, self.game.move_list + str(player) + str(column), last_move))
                successor.game.board = successor_board
                successors[successor] = self.eval_func(successor)

        if player == MAX:
            successors = sorted(successors.items(), key=operator.itemgetter(1), reverse = True)
        elif player == MIN:
            successors = sorted(successors.items(), key=operator.itemgetter(1))

        finallist = []

        for element in successors:
            finallist.append(element[0])

        return finallist


def alpha_beta_search(state, player, depth_limit=4, eval_func=evaluate_using_both):
    best_move = search(state, player, depth_limit=depth_limit, eval_func=eval_func)[1]

    return best_move


def search(state, player, alpha=-math.inf, beta=math.inf, depth_limit=6, current_depth=0, eval_func=evaluate_using_both):
    """
    Performs minimax search with alpha-beta pruning. Uses a transposition table to keep track of previously seen
    states.

    :param state: A StateSpace object
    :param player: An integer indicating the player. Should always either be MIN or MAX
    :param alpha: The current value of alpha
    :param beta: The current value of beta
    :param depth_limit: The maximum depth to perform DFS to
    :param current_depth: The current depth of recursion
    :return: A tuple of the form (utility, best_move)
    """

    # Get an md5 hash of the current board to use as the key for the transposition table
    md5 = hashlib.md5(state.game.board.tostring()).hexdigest()

    # Check to see if the value if the utility value of the current state has been previously stored in the transposition
    # table. If so, simply return what is in the transposition table. If not, first check to see if the game is over.
    # If the game is over, return the proper utility based on who won. Store this utility value in the transposition
    # table
    if current_depth != 0:
        cache_result = CACHE.get(md5)
        if cache_result is not None:
            # Case when state utility value has been cached in the transposition table.
            return cache_result[0], cache_result[1]
        else:
            # Case state utility hasn't yet been cached.
            check_game_over = state.game.checkForWin()

            if check_game_over != connect_four.NOT_OVER:
                CACHE[md5] = (check_game_over, state.game.last_move)
                return check_game_over, state.game.last_move
                # return check_game_over

    # If we've reached the
    # maximum search depth, then use the evaluation function to estimate the utility of the state.
    if depth_limit == current_depth:
        estimated_utility = eval_func(state)
        return estimated_utility, state.game.last_move

    # The case where player is MIN
    if player == MIN:
        best_move = None
        min_value = math.inf
        one_time = True

        # Iterate over all of the successors for the current board state and player
        for state in state.successorsSorted(player):
            # Make sure that best_move won't be None
            if one_time:
                best_move = state.game.last_move
                one_time = False

            # Recurse by switching players and increasing current depth
            state_utility, state_move = search(state, MAX, alpha, beta, depth_limit, current_depth + 1, eval_func)

            # Update the value of beta
            beta = min(beta, state_utility)

            # This performs a beta cut
            if alpha >= beta:
                return beta, state.game.last_move

            # Updates the minimum utility
            if state_utility < min_value:
                min_value = state_utility
                best_move = state.game.last_move

        return min_value, best_move
    # The case where player is MAX
    else:
        best_move = None
        max_value = -math.inf
        one_time = True

        # Iterate over all of the successors for the current board state and player
        for state in state.successorsSorted(player):
            # Make sure that best_move won't be None
            if one_time:
                best_move = state.game.last_move
                one_time = False

            # Recurse by switching players and increasing current depth
            state_utility, state_move = search(state, MIN, alpha, beta, depth_limit, current_depth + 1, eval_func)

            # Update the value of alpha
            alpha = max(alpha, state_utility)

            # This performs an alpha cut
            if alpha >= beta:
                return alpha, state.game.last_move

            # Updates the maximum utility
            if state_utility > max_value:
                max_value = state_utility
                best_move = state.game.last_move

        return max_value, best_move


def save_cache():
    pickle.dump(CACHE, open("transposition_tables/transposition_table", "wb"))


def load_cache():
    global CACHE

    CACHE = pickle.load(open("transposition_tables/transposition_table", "rb"))
