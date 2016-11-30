import numpy as np

NONE = 0
PLAYER = -1
COMPUTER = 1

EVALUATION_TABLE = np.array(
    [[3, 4, 5, 7, 5, 4, 3], [4, 6, 8, 10, 8, 6, 4], [5, 8, 11, 13, 11, 8, 5], [5, 8, 11, 13, 11, 8, 5],
     [4, 6, 8, 10, 8, 6, 4], [3, 4, 5, 7, 5, 4, 3]])

def evaluate_based_on_location_ratings(state):
    utility = 138
    sum = 0

    for i in range(state.game.rows):
        for j in range(state.game.cols):
            if state.game.board[i][j] == PLAYER:
                sum -= EVALUATION_TABLE[i][j]
            if state.game.board[i][j] == COMPUTER:
                sum += EVALUATION_TABLE[i][j]

    return sum + utility