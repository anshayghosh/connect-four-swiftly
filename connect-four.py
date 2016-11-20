#! /usr/bin/env python3
from itertools import groupby, chain
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

NONE = 0
PLAYER = 1
COMPUTER = -1

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
        self.board = [[NONE] * rows for _ in range(cols)]

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

    def checkForWin (self):
        """Check the current board for a winner."""
        w = self.getWinner()
        if w:
            self.printBoard()
            print(w + ' won!')
            return True
        return False

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


if __name__ == '__main__':
    g = Game()
    turn = PLAYER
    while True:
        g.printBoard()
        row = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))
        while (g.insert(int(row), turn) == False):
            print("Column is full")
            row = input('{}\'s turn: '.format('Player' if turn == PLAYER else 'Computer'))
        if (g.checkForWin()):
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()