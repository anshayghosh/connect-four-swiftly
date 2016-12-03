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

class Game:
    def __init__ (self, cols = 7, rows = 6, requiredToWin = 4, move_list="", last_move = []):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        # self.board = [[NONE] * rows for _ in range(cols)]
        self.board = np.zeros([rows, cols])
        self.move_list = move_list  # A string to keep track of the current moves leading to the current board state
        self.last_move = last_move

    def insert (self, column, color):
        """Insert the color in the given column."""
        c = self.board[:, column]
        if c[0] != NONE:
            return False
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
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
    g = Game()
    turn = PLAYER
    while True:
        g.printBoard()

        if (turn == COMPUTER):
            state = minimax_search.StateSpace(g)
            new_state = minimax_search.search(state, MAX)[1]

            # cProfile.runctx('minimax_search.search(state, MAX)[1]', {"state": state, "minimax_search":minimax_search, "MAX":MAX}, {})
            if new_state is not None:
                print("computer turn")
                g.insert(int(new_state.game.move_list[-1][-1:]), turn)
                #g.board = new_state.game.board
                #g.move_list = new_state.game.move_list
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
            break
        turn = COMPUTER if turn == PLAYER else PLAYER
        cls()


if __name__ == '__main__':
    main()
