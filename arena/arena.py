import numpy as np

class Game:
    def __init__(self, n = 19):
        self.n = n
        self.current_player = 1 # NOTE: what happen in case of handicap?
        self.board = Board(self.n)

class Board:
    def __init__(self, n = 19):
        self.n = n
        self.board = np.zeros((n, n))
        self.liberties = np.zeros((n, n))

    def move(self, x, y):
        if x >= 0 and x < self.n and y >= 0 and y < self.n:
            if self.board[x][y] == 0: # 1: black, -1: white, 0: empty
                self.board[x][y] = self.current_player
                # update liberties and compute captures
                self.compute_captures_from_last_move(x, y)
                self.upda
                self.current_player *= -1
            else:
                raise Exception('move was played before')
        else:
            raise Exception('move outside the board')

    def remove_captured_stones(self, x, y, curr, opp, stones = None):
        if stones is None:
            stones = set()
        # remove stone
        self.board[x][y] == 0
        stones.add((x,y))
        # check neighboors (connected stones)
        if x - 1 >= 0 and self.board[x - 1][y] == opp and (x - 1, y) not in stones:
            self.remove_captured_stones(x - 1, y, curr, opp, stones)
        if x + 1 < self.n and self.board[x + 1][y] == opp and (x + 1, y) not in stones:
            self.remove_captured_stones(x + 1, y, curr, opp, stones)
        if y - 1 >= 0 and self.board[x][y - 1] == opp and (x, y - 1) not in stones:
            self.remove_captured_stones(x, y - 1, curr, opp, stones)
        if y + 1 < self.n and self.board[x][y + 1] == opp and (x, y + 1) not in stones:
            self.remove_captured_stones(x, y + 1, curr, opp, stones)

    def compute_captures_from_last_move(self, x, y):
        curr = self.current_player
        opp = -curr
        # in board, opponent stone and only one liberty
        if x - 1 >= 0 and self.board[x - 1][y] == opp and self.liberties[x - 1][y] == 1:
            self.remove_captured_stones(x - 1, y, curr, opp)
        if x + 1 < self.n and self.board[x + 1][y] == opp and self.liberties[x + 1][y] == 1:
            self.remove_captured_stones(x + 1, y, curr, opp)
        if y - 1 >= 0 and self.board[x][y - 1] == opp and self.liberties[x][y - 1] == 1:
            self.remove_captured_stones(x, y - 1, curr, opp)
        if y + 1 < self.n and self.board[x][y + 1] == opp and self.liberties[x][y + 1] == 1:
            self.remove_captured_stones(x, y + 1, curr, opp)

    def compute_num_of_liberties(self, x, y, stones, liberties = None):
        if liberties is None:
            liberties = set()
        if (x, y) in stones:
            return 0
        stones.add((x, y))
        if x - 1 >= 0:
            if self.board[x - 1][y] == 0:
                liberties.add((x - 1, y))
            elif self.board[x][y] == self.board[x - 1][y]:
                self.compute_num_of_liberties(x - 1, y, stones, liberties)
        if x + 1 < self.n:
            if self.board[x + 1][y] == 0:
                liberties.add((x + 1, y))
            elif self.board[x][y] == self.board[x + 1][y]:
                self.compute_num_of_liberties(x + 1, y, stones, liberties)
        if y - 1 >= 0:
            if self.board[x][y - 1] == 0:
                liberties.add((x, y - 1))
            elif self.board[x][y] == self.board[x][y - 1]:
                self.compute_num_of_liberties(x, y - 1, stones, liberties)
        if y + 1 < self.n:
            if self.board[x][y + 1] == 0:
                liberties.add((x, y + 1))
            elif self.board[x][y] == self.board[x][y + 1]:
                self.compute_num_of_liberties(x, y + 1, stones, liberties)
        return len(liberties)

    def update_liberties(self):
        stones = set()
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    self.liberties[i][j] = 0
                elif (i, j) not in stones:
                    self.liberties[i][j] = self.compute_num_of_liberties(i, j, stones)