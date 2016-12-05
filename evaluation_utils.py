import numpy as np
import sys


# INTEGER VALUES REPRESENTING EACH DIFFERENT KIND OF "COLOR" IN A SQUARE ON THE BOARD
NONE = 0
PLAYER = -1
COMPUTER = 1


# Evaluation table is used to represent the number of possible ways of winning
# from a specific square on the board for ex: corners will have only 3 because there are only
# 3 possible ways to win wherein the connected 4 includes a corner square

EVALUATION_TABLE = np.array(
    [[3, 4, 5, 7, 5, 4, 3], [4, 6, 8, 10, 8, 6, 4], [5, 8, 11, 13, 11, 8, 5], [5, 8, 11, 13, 11, 8, 5],
     [4, 6, 8, 10, 8, 6, 4], [3, 4, 5, 7, 5, 4, 3]])


# used for checking wheiher the row,col pair is outside the board or not. 
BORDER_COLUMN = 6

BORDER_ROW = 5


# used to iterate through all the directions possible from a square on the board
# a direction pair is represneted by DT[0][0], DT[1][0] which is 0,1 which is
# the northern direction and the negative would be the southern direction and since there
# are 8 possible directions in connect 4, there are 4 pairs and negative for each, which makes 8
DIRECTION_TABLE = [[0,1,1,-1],[1,1,0,1]]


# the weights for measureing how much power a state has based on how many dots the player
# has in a row. 
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
    """
    Calculate the estimated utility of a given state by iterating over all cells of the board,
    and using the directional table to navigate to each different direction from the cell to
    get the actual length of the current chain (number of dots the player has in a row) and getting the
    corresponding weight, which would be the index of the weights list and making sure all cells are visited
    and the corresponding total is returned. 
    """
    # initializing the visited array to all false values as none of the cells are visited before the
    # beginning of the loop
    visited = []
    for row in range(0,6):
        temp = []
        for col in range(0,7):
            temp.append(False)
        visited.append(temp)

    final = 0

    # iterating over each row and column of the board
    for row in range(0,6):
        for col in range(0,7):
            # check if the row, col pair has been visited prior
            if(not (visited[row][col])):
                # get the current color on the cell which could be 0, -1 or 1
                color = state.game.board[row][col]
                # check if one of the players has placed a dot on the current cell
                if(color != NONE):
                    # run loop for the directional table
                    for i in range(0,4):
                        # get all 8 values from different directions and evaluate: 
                        actual1, potential1 = getActualAndPotentialLength(state, row, col, DIRECTION_TABLE[0][i], DIRECTION_TABLE[1][i],visited)
                        actual2, potential2 = getActualAndPotentialLength(state, row, col, -DIRECTION_TABLE[0][i], -DIRECTION_TABLE[1][i],visited)

                        # add the actual lengths up of the two opposite directions to get the total length of the current chain
                        current = actual1 + actual2

                        # check if the current chain has the potential to be a winning chain and add to the total
                        if(potential1 + potential2 >= 3):
                            try:
                                final = final + color * weights[current]
                            except IndexError:
                                print([actual1, actual2, potential1, potential2], file=sys.stderr)
                #show that the current node has been visited 
                visited[row][col]=True
    return final


def evaluate_using_both(state):
    """
    Estimate the current utility of the state by adding the two previous utility functions
    """
    total = 0
    total = total + evaluate_based_on_location_ratings(state)
    total = total + evaluate_using_lengths(state)

    return total 

#========================  HELPER FUNCTIONS  ==================================================



def positionCheck(row,col, color, state):
    """
    simple boolean helper to check if the row and col pair are within the bounds and the color inputted
    is the same as the one on the cell in state at the row, col pair provided
    """
    if(col<= BORDER_COLUMN and row <= BORDER_ROW and row>=0 and col>=0 and state.game.board[row][col] == color):
        return True
    else:
        return False


def getActualAndPotentialLength(state, row, col, dir1, dir2, visited):
    """
    Helper function that uses the directions provided and appends the current row and colum
    to check how far the current chain is going and then to check the current chain's potential
    which is how far it could possibly go without being blocked by a wall or by a another player's
    connect 4 unit
    """
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
