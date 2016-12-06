#! /usr/bin/env python3
from itertools import groupby, chain
import os
import cProfile
import numpy as np
import minimax_search
import math
import cProfile
from evaluation_utils import *

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

NONE = 0
PLAYER = -1
COMPUTER = 1

TIE = 0
NOT_OVER = -5000

MIN = -1
MAX = 1

#base game taken from https://gist.github.com/poke/6934842
#changed to use numpy
#additional variables were added, and checking for wins was made significantly faster
#main() and other functions outside of Game class were added/changed to support CPU players

class Game:
    def __init__ (self, cols = 7, rows = 6, requiredToWin = 4, move_list="", last_move = []):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        # self.board = [[NONE] * rows for _ in range(cols)]
        self.board = np.zeros([rows, cols])
        self.move_list = move_list  # A string to keep track of the current moves leading to the current board state
        self.last_move = last_move # An list of shape [row, col] indicating the cell where the last token was placed
        self.full = np.zeros([cols])

    def insert (self, column, color):
        """Insert the color in the given column."""
        c = self.board[:, column]
        if c[0] != NONE:
            return False
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
        if c[0] != NONE:
            self.full[column] = 1
        self.move_list += str(color) + str(column)
        self.last_move = [c.size + i, column]

        return True

    def simulate_insert(self, column, color):
        """Similar to insert except that it doesn't modify the current game board. Instead, it generates an entirely new
        board. This method is used for generated successors in the minimax_search.py file"""
        board_copy = np.copy(self.board)

        c = board_copy[:, column]
        if c[0] != NONE:
            return board_copy, self.last_move
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
        # self.last_move = [c.size + i, column]
        last_move = [c.size + i, column]

        return board_copy, last_move

    def checkForWin (self):
        """Check the current board for a winner."""
        if self.last_move == []:
            return NOT_OVER

        w = self.getWinner()
        if w == PLAYER:
            # self.printBoard()
            # print(str(w) + ' won!')
            return - 9999
        elif w == COMPUTER:
            # self.printBoard()
            # print(str(w) + ' won!')
            return 9999

        # self.printBoard()
        if not (self.board != 0).all():
            return NOT_OVER

        return TIE

    def getWinner (self):
        """Get the winner on the current board."""
        lines = (
            self.board[:, self.last_move[1]].tolist(), # columns
            self.lastPlayedRow(self.board, self.cols, self.rows), # rows
            self.lastPlayedDiagonalPos(self.board, self.cols, self.rows), # positive diagonals
            self.lastPlayedDiagonalNeg(self.board, self.cols, self.rows) # negative diagonals
        )

        colour = self.board[self.last_move[0], self.last_move[1]]
        for line in lines:
            count = 0
            for var in line:
                if var == colour:
                    count += 1
                    if count == 4:
                        return colour
                else:
                    count = 0

    def printBoard (self):
        """Print the board."""
        print('  '.join(map(str, range(self.cols))))
        for x in range(self.rows):
            s = ""
            for y in range(self.cols):
                if self.board[x][y] == NONE:
                    s += "  0"
                if self.board[x][y] == PLAYER:
                    s += "  P"
                if self.board[x][y] == COMPUTER:
                    s += "  C"
            #print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
            print(s[2:])
        print()        
        
    def lastPlayedRow (self, matrix, cols, rows):
            """Get rows."""
            board = self.board.tolist()
            rowList = []
            col = 0
            row = self.last_move[0]
            while (col < cols):
                rowList.append(board[row][col])
                col += 1
            return rowList       

    def lastPlayedDiagonalPos (self, matrix, cols, rows):
        """Get positive diagonals, going from bottom-left to top-right."""
        board = self.board.tolist()
        diag = []
        col = self.last_move[1]
        row = self.last_move[0]
        while (col > 0 and row > 0):
            col -= 1
            row -= 1
        while (col < cols and row < rows):
            diag.append(board[row][col])
            col += 1
            row += 1
        return diag
    
    def lastPlayedDiagonalNeg (self, matrix, cols, rows):
        """Get positive diagonals, going from bottom-left to top-right."""
        board = self.board.tolist()
        diag = []
        col = self.last_move[1]
        row = self.last_move[0]
        while (col > 0 and col < cols - 1 and row > 0 and row < rows - 1):
            col -= 1
            row += 1
        while (col >= 0 and col < cols and row >= 0 and row < rows):
            diag.append(board[row][col])
            col += 1
            row -= 1
        return diag

def printBoardToFile (file, board):
    """Print the board."""
    file.write('  '.join(map(str, range(0, len(board[0])))) + "\n")
    for x in range(0, len(board)):
        s = ""
        for y in range(0, len(board[0])):
            if board[x][y] == NONE:
                s += "  0"
            if board[x][y] == PLAYER:
                s += "  P"
            if board[x][y] == COMPUTER:
                s += "  C"
        file.write(s[2:] + "\n")
    file.write("\n")

def main():
    minimax_search.load_cache()
    g = Game()
    turn = PLAYER
    while True:
        g.printBoard()

        if (turn == COMPUTER):
            state = minimax_search.StateSpace(g)
            print("computer turn")
            # new_state = minimax_search.search(state, MAX)[1]
            new_move = minimax_search.alpha_beta_search(state, MAX)

            # cProfile.runctx('minimax_search.search(state, MAX)[1]', {"state": state, "minimax_search":minimax_search, "MAX":MAX}, {})
            # input("Enter")
            # if new_state is not None:
            #     print("computer turn")
            #     g.insert(int(new_state.game.move_list[-1][-1:]), turn)
            #     #g.board = new_state.game.board
            #     #g.move_list = new_state.game.move_list
            if new_move is not None:
                g.insert(new_move[1], turn)
        else:
            col = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))
            if col == '':
                break
            row = g.insert(int(col), turn)
            while (row == False):
                print("Column is full")
                col = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))
                row = g.insert(int(col), turn)

        win_check_result = g.checkForWin()
        if (win_check_result != NOT_OVER):
            # print(g.checkForWin())
            g.printBoard()
            if win_check_result == 9999:
                print("Computer won!")
            elif win_check_result == -9999:
                print("Player won!")
            else:
                print("Tie Game!")

            minimax_search.save_cache()
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()


def computer_vs_computer(p1_initial_moves=[], p2_initial_moves=[], p1_diff=3, p2_diff=3, eval_func1=evaluate_using_both, eval_func2=evaluate_using_both):
    g = Game()
    turn = PLAYER

    for i in range(len(p1_initial_moves)):
        g.insert(p1_initial_moves[i], turn)
        turn = COMPUTER if turn == PLAYER else PLAYER

        win_check_result = g.checkForWin()
        if (win_check_result != NOT_OVER):
            #g.printBoard()
            if win_check_result == 9999:
                print("Computer won!")
                return False
            elif win_check_result == -9999:
                print("Player won!")
                return False
            else:
                print("Tie Game!")
                return False
            return

        g.insert(p2_initial_moves[i], turn)
        turn = COMPUTER if turn == PLAYER else PLAYER

        win_check_result = g.checkForWin()
        if (win_check_result != NOT_OVER):
            #g.printBoard()
            if win_check_result == 9999:
                print("Computer won!")
                return False
            elif win_check_result == -9999:
                print("Player won!")
                return False
            else:
                print("Tie Game!")
                return False
            return


    while True:
        #g.printBoard()

        if (turn == COMPUTER):
            state = minimax_search.StateSpace(g, eval_func=eval_func1)
            #print("computer turn")
            new_move = minimax_search.alpha_beta_search(state, MAX, depth_limit=p1_diff, eval_func=eval_func1)


            if new_move is not None:
                g.insert(new_move[1], turn)
        else:
            state = minimax_search.StateSpace(g, eval_func=eval_func1)
            #print("player turn")
            new_move = minimax_search.alpha_beta_search(state, MAX, depth_limit=p2_diff, eval_func=eval_func2)


            if new_move is not None:
                g.insert(new_move[1], turn)

        win_check_result = g.checkForWin()
        if (win_check_result != NOT_OVER):
            #g.printBoard()
            if win_check_result == 9999:
                print("Computer won!")
                return COMPUTER, g.board
            elif win_check_result == -9999:
                print("Player won!")
                return PLAYER, g.board
            else:
                print("Tie Game!")
                return TIE, g.board

            minimax_search.save_cache()
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()

def grid_search(difficulty_levels=[1, 2, 3, 4], rand_moves=5, eval_func1=evaluate_using_both, eval_func2=evaluate_using_both):
    """
    Tries a bunch of different settings for different search depths, combined with random initial moves
    """
    minimax_search.load_cache()
    difficulties = difficulty_levels
    
    results = []

    for p1_diff in difficulties:
        for p2_diff in difficulties:
            initial_moves_p1 = np.random.random_integers(0, 6, rand_moves)
            initial_moves_p2 = np.random.random_integers(0, 6, rand_moves)
            results.append(computer_vs_computer(list(initial_moves_p1), list(initial_moves_p2), p1_diff, p2_diff, eval_func1=eval_func1, eval_func2=eval_func2))
    return results

LOCATION = evaluate_based_on_location_ratings
LENGTH = evaluate_using_lengths
BOTH = evaluate_using_both

def eval_func_to_string(func):
    if func == LOCATION:
        return "locations"
    elif func == LENGTH:
        return "lengths"
    elif func == BOTH:
        return "both"

def test_no_random_moves(final_scores):
    test_no = 1
    while os.path.isfile("final_boards_no_random_moves" + str(test_no) + ".txt"):
        test_no += 1      
    with open("final_boards_no_random_moves" + str(test_no) + ".txt", 'w', 1) as final_boards_no_random_moves:
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, LOCATION, LOCATION)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, LOCATION, LENGTH)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, LENGTH, LOCATION)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, LOCATION, BOTH)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, BOTH, LOCATION)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, LENGTH, LENGTH)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, LENGTH, BOTH)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, BOTH, LENGTH)
        single_test_no_random_moves(final_scores, final_boards_no_random_moves, BOTH, BOTH)
    
def single_test_no_random_moves(final_scores, final_boards_no_random_moves, eval_func1, eval_func2):
    for depth in range(1, 7):
        scores = [0] * 3
        for i in range(0, 20):
            result = computer_vs_computer(p1_diff=depth, p2_diff=depth, eval_func1=eval_func1, eval_func2=eval_func2)
            if result[0] == PLAYER:
                final_boards_no_random_moves.write("Winner: " + eval_func_to_string(eval_func1) + ", Loser: " + eval_func_to_string(eval_func2) + "\n")
                scores[0] += 1
            elif result[0] == COMPUTER:
                final_boards_no_random_moves.write("Loser: " + eval_func_to_string(eval_func1) + ", Winner: " + eval_func_to_string(eval_func2) + "\n")
                scores[1] += 1
            elif result[0] == TIE:
                final_boards_no_random_moves.write("Tie: " + eval_func_to_string(eval_func1) + ", " + eval_func_to_string(eval_func2) + "\n")
                scores[2] += 1
            final_boards_no_random_moves.write(" Depth: " + str(depth) + "\n")
            printBoardToFile(final_boards_no_random_moves, result[1])
            final_boards_no_random_moves.write("\n")
        final_scores.write("Score: " + eval_func_to_string(eval_func1) + ": " + str(scores[0]) + "  " + eval_func_to_string(eval_func2) + ": " + str(scores[1]) + "  Ties: " + str(scores[2]) + "    Depth was:" + str(depth) + "\n")
    final_scores.write("\n")
    
def test_n_random_moves(final_scores, rand_moves=5, difficulty_levels=[1, 2, 3, 4]):
    test_no = 1
    while os.path.isfile("final_boards_n_random_moves" + str(test_no) + ".txt"):
        test_no += 1  
    with open("final_boards_n_random_moves" + str(test_no) + ".txt", 'w', 1) as final_boards_n_random_moves:
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, LOCATION, LOCATION, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, LOCATION, LENGTH, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, LENGTH, LOCATION, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, LOCATION, BOTH, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, BOTH, LOCATION, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, LENGTH, LENGTH, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, LENGTH, BOTH, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, BOTH, LENGTH, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        single_test_n_random_moves(final_scores, final_boards_n_random_moves, BOTH, BOTH, rand_moves=rand_moves, difficulty_levels=difficulty_levels)
        
def single_test_n_random_moves(final_scores, final_boards_n_random_moves, eval_func1, eval_func2, rand_moves=5, difficulty_levels=[1, 2, 3, 4]):
    for difficulty in difficulty_levels:
        scores = [0] * 3
        for i in range(0, 20):
            result = grid_search(difficulty_levels=[difficulty], rand_moves=rand_moves, eval_func1=eval_func1, eval_func2=eval_func2)
            while result[0] == False:
                result = grid_search(difficulty_levels=[difficulty], eval_func1=eval_func1, eval_func2=eval_func2)  
            if result[0][0] == PLAYER:
                final_boards_n_random_moves.write("Winner: " + eval_func_to_string(eval_func1) + ", Loser: " + eval_func_to_string(eval_func2) + "\n")
                scores[0] += 1
            elif result[0][0] == COMPUTER:
                final_boards_n_random_moves.write("Loser: " + eval_func_to_string(eval_func1) + ", Winner: " + eval_func_to_string(eval_func2) + "\n")
                scores[1] += 1
            elif result[0][0] == TIE:
                final_boards_n_random_moves.write("Tie: " + eval_func_to_string(eval_func1) + ", " + eval_func_to_string(eval_func2) + "\n")
                scores[2] += 1
            final_boards_n_random_moves.write(" Depth: " + str(difficulty) + "\n")
            printBoardToFile(final_boards_n_random_moves, result[0][1])
            final_boards_n_random_moves.write("\n")
        final_scores.write("Score: " + eval_func_to_string(eval_func1) + ": " + str(scores[0]) + "  " + eval_func_to_string(eval_func2) + ": " + str(scores[1]) + "  Ties: " + str(scores[2]) + "    Depth was:" + str(difficulty) + "  random moves:" + str(rand_moves) + "\n")
    final_scores.write("\n")


if __name__ == '__main__':
    #main(), computer_vs_computer(), grid_search()
    
    test_no = 1
    while os.path.isfile("final_scores" + str(test_no) + ".txt"):
        test_no += 1
    with open("final_scores" + str(test_no) + ".txt", 'w', 1) as final_scores:
        test_no_random_moves(final_scores)
        test_n_random_moves(final_scores, rand_moves=5, difficulty_levels=[1, 2, 3, 4, 5, 6])