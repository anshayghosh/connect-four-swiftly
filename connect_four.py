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
NOT_OVER = -99

MIN = -1
MAX = 1


def diagonalsPos (matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows -1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

def diagonalsNeg (matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

class Game:
    def __init__ (self, cols = 7, rows = 6, requiredToWin = 4, move_list=""):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        # self.board = [[NONE] * rows for _ in range(cols)]
        self.board = np.zeros([cols, rows])
        self.move_list = move_list  # A string to keep track of the current moves leading to the current board state

    def insert (self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            return False
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
        self.move_list += str(color) + str(column)

        return True

    def simulate_insert(self, column, color):
        """Similar to insert except that it doesn't modify the current game board. Instead, it generates an entirely new
        board. This method is used for generated successors in the minimax_search.py file"""
        board_copy = np.copy(self.board)

        c = board_copy[column]
        if c[0] != NONE:
            return board_copy
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color

        return board_copy

    def checkForWin (self):
        """Check the current board for a winner."""
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
            self.board, # columns
            zip(*self.board), # rows
            diagonalsPos(self.board, self.cols, self.rows), # positive diagonals
            diagonalsNeg(self.board, self.cols, self.rows) # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    def printBoard (self):
        """Print the board."""
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            s = ""
            for x in range(self.cols):
                if self.board[x][y] == NONE:
                    s += "  0"
                if self.board[x][y] == PLAYER:
                    s += "  P"
                if self.board[x][y] == COMPUTER:
                    s += "  C"
            #print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
            print(s[2:])
        print()


def main():
    g = Game()
    turn = PLAYER
    while True:
        g.printBoard()

        if (turn == COMPUTER):
            state = minimax_search.StateSpace(g)
            new_state = minimax_search.search(state, MAX)[1]

            # cProfile.runctx('minimax_search.search(state, MAX)[1]', {"state": state, "minimax_search":minimax_search, "MAX":MAX}, {})
            if new_state is not None:
                g.board = new_state.game.board
                g.move_list = new_state.game.move_list
        else:
            row = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))
            if row == '':
                break
            while (g.insert(int(row), turn) == False):
                print("Column is full")
                row = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))

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
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()


if __name__ == '__main__':
    main()
