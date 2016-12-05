import numpy as np
import sys

NONE = 0
PLAYER = -1
COMPUTER = 1

EVALUATION_TABLE = np.array(
    [[3, 4, 5, 7, 5, 4, 3], [4, 6, 8, 10, 8, 6, 4], [5, 8, 11, 13, 11, 8, 5], [5, 8, 11, 13, 11, 8, 5],
     [4, 6, 8, 10, 8, 6, 4], [3, 4, 5, 7, 5, 4, 3]])


BORDER_COLUMN = 6

BORDER_ROW = 5

DIRECTION_TABLE = [[0,1,1,-1],[1,1,0,1]]

weights = [0,50,500]

#======================= INDIVIDUAL EVALUATION FUNCTIONS ==========================================

def evaluate_based_on_location_ratings(state):
    """"
    Calculates the estimated utility of a given state by iterating over all cells of the board, checking who has
    control of the cells that are occupied by tokens, and adding up the usefulness of each sell. Note that this is
    made so that a positive utility is returned if the computer has a better chance of winning, and a negative utility
    is returned if the player has a better chance of winning.

    :param state: A StateSpace object
    :return: Positive value if computer is more likely to win, negative value if player is more likely to win, 0 if both
             players are equally likely to win
    """
    sum = 0

    for i in range(state.game.rows):
        for j in range(state.game.cols):
            if state.game.board[i][j] == PLAYER:
                sum -= EVALUATION_TABLE[i][j]
            if state.game.board[i][j] == COMPUTER:
                sum += EVALUATION_TABLE[i][j]

    return sum




def evaluate_using_lengths(state):
    visited = []
    for row in range(0,6):
        temp = []
        for col in range(0,7):
            temp.append(False)
        visited.append(temp)

    final = 0


    for row in range(0,6):
        for col in range(0,7):
            if(not (visited[row][col])):
                color = state.game.board[row][col]
                if(color != NONE):
                    for i in range(0,4):
                        actual1, potential1 = getActualAndPotentialLength(state, row, col, DIRECTION_TABLE[0][i], DIRECTION_TABLE[1][i],visited)
                        actual2, potential2 = getActualAndPotentialLength(state, row, col, -DIRECTION_TABLE[0][i], -DIRECTION_TABLE[1][i],visited)

                        current = actual1 + actual2
                        if(potential1 + potential2 >= 3):
                            try:
                                final = final + color * weights[current]
                            except IndexError:
                                print([actual1, actual2, potential1, potential2], file=sys.stderr)

                visited[row][col]=True
    return final

def evaluate_using_both(state):
    total = 0
    total = total + evaluate_based_on_location_ratings(state)
    total = total + evaluate_using_lengths(state)

    return total 

#========================  HELPER FUNCTIONS  ==================================================

def positionCheck(row,col, color, state):
    if(col<= BORDER_COLUMN and row <= BORDER_ROW and row>=0 and col>=0 and state.game.board[row][col] == color):
        return True
    else:
        return False


def getActualAndPotentialLength(state, row, col, dir1, dir2, visited):
    length = 1
    color = state.game.board[row][col]

    while(positionCheck(row + (dir1 * length), col + (dir2 * length), color, state)):
        visited[row + (dir1 * length)][col + (dir2 * length)] = True
        length = length + 1

    actual = length - 1

    while(positionCheck(row + (dir1 * length), col + (dir2 * length), NONE, state)):
        visited[row + (dir1 * length)][col + (dir2 * length)] = True
        length = length + 1


    return actual - 1, length - 1