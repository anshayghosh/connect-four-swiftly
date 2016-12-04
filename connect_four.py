#! /usr/bin/env python3
from itertools import groupby, chain
import os
import cProfile
import numpy as np
import minimax_search
import math
import cProfile

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

NONE = 0
PLAYER = -1
COMPUTER = 1

TIE = 0
NOT_OVER = -5000

MIN = -1
MAX = 1        

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
            return - math.inf
        elif w == COMPUTER:
            # self.printBoard()
            # print(str(w) + ' won!')
            return math.inf

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
            if win_check_result == math.inf:
                print("Computer won!")
            elif win_check_result == -math.inf:
                print("Player won!")
            else:
                print("Tie Game!")

            minimax_search.save_cache()
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()


def computer_vs_computer(p1_initial_moves=[], p2_initial_moves=[], p1_diff=3, p2_diff=3):
    g = Game()
    turn = PLAYER

    for i in range(len(p1_initial_moves)):
        g.insert(p1_initial_moves[i], turn)
        turn = COMPUTER if turn == PLAYER else PLAYER

        win_check_result = g.checkForWin()
        if (win_check_result != NOT_OVER):
            # print(g.checkForWin())
            g.printBoard()
            if win_check_result == math.inf:
                print("Computer won!")
            elif win_check_result == -math.inf:
                print("Player won!")
            else:
                print("Tie Game!")
            return

        g.insert(p2_initial_moves[i], turn)
        turn = COMPUTER if turn == PLAYER else PLAYER

        win_check_result = g.checkForWin()
        if (win_check_result != NOT_OVER):
            # print(g.checkForWin())
            g.printBoard()
            if win_check_result == math.inf:
                print("Computer won!")
            elif win_check_result == -math.inf:
                print("Player won!")
            else:
                print("Tie Game!")
            return


    while True:
        g.printBoard()

        if (turn == COMPUTER):
            state = minimax_search.StateSpace(g)
            print("computer turn")
            new_move = minimax_search.alpha_beta_search(state, MAX)


            if new_move is not None:
                g.insert(new_move[1], turn)
        else:
            state = minimax_search.StateSpace(g)
            print("player turn")
            new_move = minimax_search.alpha_beta_search(state, MAX, depth_limit=4)


            if new_move is not None:
                g.insert(new_move[1], turn)

        win_check_result = g.checkForWin()
        if (win_check_result != NOT_OVER):
            # print(g.checkForWin())
            g.printBoard()
            if win_check_result == math.inf:
                print("Computer won!")
            elif win_check_result == -math.inf:
                print("Player won!")
            else:
                print("Tie Game!")

            minimax_search.save_cache()
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()

def grid_search():
    """
    Tries a bunch of different settings for different search depths, combined with random initial moves
    """
    minimax_search.load_cache()
    difficulties = [1,2,3,4]

    for p1_diff in difficulties:
        for p2_diff in difficulties:
            initial_moves_p1 = np.random.random_integers(0, 6, 5)
            initial_moves_p2 = np.random.random_integers(0, 6, 5)
            computer_vs_computer(list(initial_moves_p1), list(initial_moves_p2), p1_diff, p2_diff)



if __name__ == '__main__':
    main()
    # computer_vs_computer()
    # grid_search()
