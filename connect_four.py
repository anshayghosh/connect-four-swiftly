#! /usr/bin/env python3
from itertools import groupby, chain
import os
import cProfile
import numpy as np
import minimax_search
import math
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

NONE = 0
PLAYER = 1
COMPUTER = -1

TIE = 0

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
    def __init__ (self, cols = 7, rows = 6, requiredToWin = 4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        # self.board = [[NONE] * rows for _ in range(cols)]
        self.board = np.zeros([cols, rows])

    def insert (self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            return False
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color

        return True

    def simulate_insert(self, column, color):
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
            self.printBoard()
            print(str(w) + ' won!')
            return - math.inf
        elif w == COMPUTER:
            self.printBoard()
            print(str(w) + ' won!')
            return math.inf

        # self.printBoard()
        if not (self.board != 0).all():
            return None

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


    def generate_successors(self, player):
        successors = []

        if player == MIN:
            token = PLAYER
        else:
            token = COMPUTER

        for i in range(self.cols):
            next_state = self.simulate_insert(i, token)

            if not (np.array_equal(self.board, next_state)):
                successors.append(next_state)

        return successors


def check_for_win(game):
    w = get_winner(game.board, game.win)
    if w == PLAYER:
        return - math.inf
    elif w == COMPUTER:
        return math.inf

    # self.printBoard()
    if not (game.board != 0).all():
        return None

    return TIE


def get_winner(board, required_to_win):
    lines = (
        board,  # columns
        zip(*board),  # rows
        diagonalsPos(board, board.shape[0], board.shape[1]),  # positive diagonals
        diagonalsNeg(board, board.shape[0], board.shape[1])  # negative diagonals
    )

    for line in chain(*lines):
        for color, group in groupby(line):
            if color != NONE and len(list(group)) >= required_to_win:
                return color

def mini_func(g):
    state = minimax_search.StateSpace(g)
    minimax_search.search(state, MAX)

def main():
    g = Game()
    turn = PLAYER
    while True:
        g.printBoard()

        if (turn == COMPUTER):
            state = minimax_search.StateSpace(g)
            new_state = minimax_search.search(state, MAX)[1]

            if new_state is not None:
                g.board = new_state.game.board
        else:
            row = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))
            if row == '':
                break
            while (g.insert(int(row), turn) == False):
                print("Column is full")
                row = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))
        if (g.checkForWin() is not None):
            # print(g.checkForWin())
            # g.printBoard()
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()


if __name__ == '__main__':
    main()
