# convert sgf files to the expected policy network input format
import os
import numpy as np
import utils as ut

# constants

# plane indexes

# stone color
PLAYER_STONES = 0
OPPONENT_STONES = 1
EMPTY_INTERSECTIONS = 2

# ones
ONES = 3

# turns since
TURNS_SINCE_1 = 4
TURNS_SINCE_2 = 5
TURNS_SINCE_3 = 6
TURNS_SINCE_4 = 7
TURNS_SINCE_5 = 8
TURNS_SINCE_6 = 9
TURNS_SINCE_7 = 10
TURNS_SINCE_8 = 11

# liberties
LIBERTIES_1 = 12
LIBERTIES_2 = 13
LIBERTIES_3 = 14
LIBERTIES_4 = 15
LIBERTIES_5 = 16
LIBERTIES_6 = 17
LIBERTIES_7 = 18
LIBERTIES_8 = 19

# capture size
CAPTURE_SIZE_1 = 20
CAPTURE_SIZE_2 = 21
CAPTURE_SIZE_3 = 22
CAPTURE_SIZE_4 = 23
CAPTURE_SIZE_5 = 24
CAPTURE_SIZE_6 = 25
CAPTURE_SIZE_7 = 26
CAPTURE_SIZE_8 = 27

# self-atari size
SELF_ATARI_SIZE_1 = 28
SELF_ATARI_SIZE_2 = 29
SELF_ATARI_SIZE_3 = 30
SELF_ATARI_SIZE_4 = 31
SELF_ATARI_SIZE_5 = 32
SELF_ATARI_SIZE_6 = 33
SELF_ATARI_SIZE_7 = 34
SELF_ATARI_SIZE_8 = 35

# liberties after this move
LIBERTIES_AFTER_MOVE_1 = 36
LIBERTIES_AFTER_MOVE_2 = 37
LIBERTIES_AFTER_MOVE_3 = 38
LIBERTIES_AFTER_MOVE_4 = 39
LIBERTIES_AFTER_MOVE_5 = 40
LIBERTIES_AFTER_MOVE_6 = 41
LIBERTIES_AFTER_MOVE_7 = 42
LIBERTIES_AFTER_MOVE_8 = 43

# # ladder capture
# LADDER_CAPTURE = 44

# # ladder escape
# LADDER_ESCAPE = 45

# # sensibleness
# SENSIBLENESS = 46

# # zeros
# ZEROS = 47

# zeros
ZEROS = 44

# classes
class Plane:
    def __init__(self, n = 19, v = 0):
        self.n = n
        self.plane = np.empty([self.n,self.n], dtype = np.int)
        self.plane.fill(v)

    def set(self, x, y, v):
        self.plane[x][y] = v

    def get(self, x, y):
        return self.plane[x][y]

    def copy(self):
        q = Plane(self.n)
        np.copyto(q.plane, self.plane)
        return q

    def printPlane(self):
        print ' ',
        for i in range(self.n):
            print "abcdefghijklmnopqrstuvwxyz"[i],
        print ''
        for i in range(self.n):
            print "abcdefghijklmnopqrstuvwxyz"[i],
            for j in range(self.n):
                print self.plane[i][j],
            print ''

    def num_of_differences(self, other): # assumes integers values, float numbers have precision details
        if self.n != other.n:
            raise Exception('planes must have same size')
        diff = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.plane[i][j] != other.plane[i][j]:
                    diff += 1
        return diff

    def to_file(self, f):
        for i in range(self.n):
            for j in range(self.n):
                f.write(str(self.plane[i][j]))
                if i + j != 2*self.n - 2:
                    f.write(' ')

class StatePlanes:
    # default represent empty board
    def __init__(self, n = 19):
        self.k = 0
        self.n = n
        self.planes = []

        # player plane
        self.planes.append(Plane(n))
        self.k += 1

        # opponent plane
        self.planes.append(Plane(n))
        self.k += 1

        # empty plane
        self.planes.append(Plane(n, 1))
        self.k += 1

        # plane of ones
        self.planes.append(Plane(n, 1))
        self.k += 1

        # turns since
        for _ in range(TURNS_SINCE_1, TURNS_SINCE_8 + 1):
            self.planes.append(Plane(n))
            self.k += 1

        # liberties
        for _ in range(LIBERTIES_1, LIBERTIES_8 + 1):
            self.planes.append(Plane(n))
            self.k += 1

        # planes for capture size
        for _ in range(CAPTURE_SIZE_1, CAPTURE_SIZE_8 + 1):
            self.planes.append(Plane(n))
            self.k += 1

        # planes for self atari size
        for _ in range(SELF_ATARI_SIZE_1, SELF_ATARI_SIZE_8 + 1):
            self.planes.append(Plane(n))
            self.k += 1

        # liberties after this move
        for _ in range(LIBERTIES_AFTER_MOVE_1, LIBERTIES_AFTER_MOVE_8 + 1):
            self.planes.append(Plane(n))
            self.k += 1

        # # ladder capture
        # self.planes.append(Plane(n))
        # self.k += 1

        # # ladder escape
        # self.planes.append(Plane(n))
        # self.k += 1

        # # sensibleness
        # self.planes.append(Plane(n))
        # self.k += 1

        # zeros
        self.planes.append(Plane(n))
        self.k += 1

    def compute_captures_from_last_move(self, coord_x, coord_y):
        # in board, opponent stone and only one liberty
        if coord_x - 1 >= 0 and self.planes[OPPONENT_STONES].get(coord_x - 1, coord_y) == 1 and self.planes[LIBERTIES_1].get(coord_x - 1, coord_y) == 1:
            self.remove_captured_stones(coord_x - 1, coord_y)
        if coord_x + 1 < self.n and self.planes[OPPONENT_STONES].get(coord_x + 1, coord_y) == 1 and self.planes[LIBERTIES_1].get(coord_x + 1, coord_y) == 1:
            self.remove_captured_stones(coord_x + 1, coord_y)
        if coord_y - 1 >= 0 and self.planes[OPPONENT_STONES].get(coord_x, coord_y - 1) == 1 and self.planes[LIBERTIES_1].get(coord_x, coord_y - 1) == 1:
            self.remove_captured_stones(coord_x, coord_y - 1)
        if coord_y + 1 < self.n and self.planes[OPPONENT_STONES].get(coord_x, coord_y + 1) == 1 and self.planes[LIBERTIES_1].get(coord_x, coord_y + 1) == 1:
            self.remove_captured_stones(coord_x, coord_y + 1)

    def copy(self):
        sp = StatePlanes(self.n)
        for i in range(self.k):
            sp.planes[i] = self.planes[i].copy()
        return sp

    def remove_captured_stones(self, x, y, stones = None):
        if stones is None:
            stones = set()
        # remove stone
        self.planes[OPPONENT_STONES].set(x, y, 0)
        self.planes[EMPTY_INTERSECTIONS].set(x, y, 1)
        stones.add((x,y))
        # check neighboors (connected stones)
        if x - 1 >= 0 and self.planes[OPPONENT_STONES].get(x - 1, y) == 1 and (x - 1, y) not in stones:
            self.remove_captured_stones(x - 1, y, stones)
        if x + 1 < self.n and self.planes[OPPONENT_STONES].get(x + 1, y) == 1 and (x + 1, y) not in stones:
            self.remove_captured_stones(x + 1, y, stones)
        if y - 1 >= 0 and self.planes[OPPONENT_STONES].get(x, y - 1) == 1 and (x, y - 1) not in stones:
            self.remove_captured_stones(x, y - 1, stones)
        if y + 1 < self.n and self.planes[OPPONENT_STONES].get(x, y + 1) == 1 and (x, y + 1) not in stones:
            self.remove_captured_stones(x, y + 1, stones)

    def set_chain_liberties(self, x, y, lib, stones = None):
        if stones is None:
            stones = set()
        if (x, y) in stones:
            return
        self.set_liberty(x, y, lib)
        stones.add((x, y))
        if x - 1 >= 0 and self.have_same_color(x, y, x - 1, y):
            self.set_chain_liberties(x - 1, y, lib, stones)
        if x + 1 < self.n and self.have_same_color(x, y, x + 1, y):
            self.set_chain_liberties(x + 1, y, lib, stones)
        if y - 1 >= 0 and self.have_same_color(x, y, x, y - 1):
            self.set_chain_liberties(x, y - 1, lib, stones)
        if y + 1 < self.n and self.have_same_color(x, y, x, y + 1):
            self.set_chain_liberties(x, y + 1, lib, stones)

    def set_liberty(self, x, y, v):
        v = min(v, LIBERTIES_8 - LIBERTIES_1 + 1)
        for i in range(LIBERTIES_8 - LIBERTIES_1 + 1):
            if i == v - 1:
                self.planes[LIBERTIES_1 + i].set(x, y, 1)
            else:
                self.planes[LIBERTIES_1 + i].set(x, y, 0)

    def get_liberty(self, x, y):
        for i in range(LIBERTIES_8 - LIBERTIES_1 + 1):
            if self.planes[LIBERTIES_1 + i].get(x, y) == 1:
                return i + 1
        return 0

    def compute_num_of_liberties(self, x, y, stones, liberties = None):
        if liberties is None:
            liberties = set()
        if (x, y) in stones:
            return 0
        stones.add((x, y))
        if x - 1 >= 0:
            if self.planes[EMPTY_INTERSECTIONS].get(x - 1, y) == 1:
                liberties.add((x - 1, y))
            elif self.have_same_color(x, y, x - 1, y):
                self.compute_num_of_liberties(x - 1, y, stones, liberties)
        if x + 1 < self.n:
            if self.planes[EMPTY_INTERSECTIONS].get(x + 1, y) == 1:
                liberties.add((x + 1, y))
            elif self.have_same_color(x, y, x + 1, y):
                self.compute_num_of_liberties(x + 1, y, stones, liberties)
        if y - 1 >= 0:
            if self.planes[EMPTY_INTERSECTIONS].get(x, y - 1) == 1:
                liberties.add((x, y - 1))
            elif self.have_same_color(x, y, x, y - 1):
                self.compute_num_of_liberties(x, y - 1, stones, liberties)
        if y + 1 < self.n:
            if self.planes[EMPTY_INTERSECTIONS].get(x, y + 1) == 1:
                liberties.add((x, y + 1))
            elif self.have_same_color(x, y, x, y + 1):
                self.compute_num_of_liberties(x, y + 1, stones, liberties)
        return len(liberties)

    def update_liberty_planes(self):
        stones = set()
        for i in range(self.n):
            for j in range(self.n):
                if self.planes[EMPTY_INTERSECTIONS].get(i, j) == 1:
                    self.set_liberty(i, j, 0)
                elif (i, j) not in stones:
                    lib = self.compute_num_of_liberties(i, j, stones)
                    self.set_chain_liberties(i, j, lib)

    def have_same_color(self, x1, y1, x2, y2):
        t1 = self.planes[EMPTY_INTERSECTIONS].get(x1, y1) == 0
        t2 = self.planes[EMPTY_INTERSECTIONS].get(x2, y2) == 0
        t3 = self.planes[PLAYER_STONES].get(x1, y1) == self.planes[PLAYER_STONES].get(x2, y2)
        t4 = self.planes[OPPONENT_STONES].get(x1, y1) == self.planes[OPPONENT_STONES].get(x2, y2) # redundant, just for consistency
        return t1 and t2 and t3 and t4

    # NOTE: this function should also update the other feature planes?
    def make_move(self, x, y):
        self.planes[PLAYER_STONES].set(x, y, 1)
        self.planes[EMPTY_INTERSECTIONS].set(x, y, 0)

    def num_of_stones_in_chain(self, x, y, stones = None):
        if stones == None:
            stones = set()
        if self.planes[EMPTY_INTERSECTIONS].get(x, y) == 1:
            return 0
        if (x, y) in stones:
            return 0
        stones.add((x, y))
        if x - 1 >= 0 and self.have_same_color(x, y, x - 1, y):
            self.num_of_stones_in_chain(x - 1, y, stones)
        if x + 1 < 19 and self.have_same_color(x, y, x + 1, y):
            self.num_of_stones_in_chain(x + 1, y, stones)
        if y - 1 >= 0 and self.have_same_color(x, y, x, y - 1):
            self.num_of_stones_in_chain(x, y - 1, stones)
        if y + 1 < 19 and self.have_same_color(x, y, x, y + 1):
            self.num_of_stones_in_chain(x, y + 1, stones)
        return len(stones)

    def set_capture_size(self, x, y, n):
        n = min(n, CAPTURE_SIZE_8 - CAPTURE_SIZE_1)
        for i in range(CAPTURE_SIZE_8 - CAPTURE_SIZE_1 + 1):
            if i == n:
                self.planes[CAPTURE_SIZE_1 + i].set(x, y, 1)
            else:
                self.planes[CAPTURE_SIZE_1 + i].set(x, y, 0)

    def set_self_atari_size(self, x, y, n):
        n = min(n, SELF_ATARI_SIZE_8 - SELF_ATARI_SIZE_1)
        for i in range(SELF_ATARI_SIZE_8 - SELF_ATARI_SIZE_1 + 1):
            if i == n:
                self.planes[SELF_ATARI_SIZE_1 + i].set(x, y, 1)
            else:
                self.planes[SELF_ATARI_SIZE_1 + i].set(x, y, 0)

    def set_liberties_after_move(self, x, y, n): # i = 0 means 0 liberties
        n = min(n, LIBERTIES_AFTER_MOVE_8 - LIBERTIES_AFTER_MOVE_1)
        for i in range(LIBERTIES_AFTER_MOVE_8 - LIBERTIES_AFTER_MOVE_1 + 1):
            if i == n:
                self.planes[LIBERTIES_AFTER_MOVE_1 + i].set(x, y, 1)
            else:
                self.planes[LIBERTIES_AFTER_MOVE_1 + i].set(x, y, 0)

    def to_file(self, f):
        for plane in self.planes:
            plane.to_file(f)
            f.write(',')

# main
path = os.getcwd().split("/")[:-1]
path.append('reduced_game_records/')
path = "/".join(path)

file_counter = 0
for file in sorted(os.listdir(path)):
    # X's and Y's
    X, Y = [], []

    # parse .sgf file
    with open(path + file, 'r') as f:
        print "Reading from", path + file

        # concatenate lines removing newline characters
        moves = "".join([l.strip() for l in f.readlines()])
        # getting the moves
        moves = moves.split(";")[2:]

    x = StatePlanes()
    X.append(x)
    for i in range(len(moves) - 1):
        # generate next state.
        move = moves[i]
        color = move[0]
        coord_x = ut.letter_to_num(move[2])
        coord_y = ut.letter_to_num(move[3])
        y = (coord_x, coord_y)

        prev_state_planes = X[-1]
        x = prev_state_planes.copy()

        # plane 1 (player stone)
        # player and opponent planes change places.
        x.planes[PLAYER_STONES], x.planes[OPPONENT_STONES] = x.planes[OPPONENT_STONES], x.planes[PLAYER_STONES]

        # make move
        x.make_move(coord_x, coord_y)

        # NOTE: assumptation: one move == one turn. Think about this.
        # 8 planes for Turns since.
        x.planes[TURNS_SINCE_8].plane += x.planes[TURNS_SINCE_7].plane

        for j in range(TURNS_SINCE_7, TURNS_SINCE_1, -1):
            x.planes[j] = x.planes[j - 1]

        x.planes[TURNS_SINCE_1] = Plane(x.n)
        x.planes[TURNS_SINCE_1].set(coord_x, coord_y, 1)

        # 8 liberties planes.
        x.compute_captures_from_last_move(coord_x, coord_y)
        x.update_liberty_planes()

        # TODO: i'll probably have to refactor this way of compute liberties, capture size and self-atari
        #       if i make them class methods, maybe i can avoid copy all StatePlanes object
        #       also, making this calculations local seems to improve performance
        # 8 capture size planes
        # 8 self-atari size planes
        # 8 liberties after this move planes
        for p in range(x.n):
            for q in range(x.n):
                sp = x.copy()
                if sp.planes[EMPTY_INTERSECTIONS].get(p, q) == 0:
                    num_captured_stones = 0
                    num_stones_self_atari = 0
                    num_liberties_of_stone_after_move = 0
                else:
                    sp.make_move(p, q) # only alters PLAYER_STONES and EMPTY_INTERSECTIONS planes
                    sp.compute_captures_from_last_move(p, q) # only alters OPPONENT_STONES plane
                    num_captured_stones = sp.planes[OPPONENT_STONES].num_of_differences(x.planes[OPPONENT_STONES])
                    sp.update_liberty_planes()
                    num_liberties_of_stone_after_move = sp.get_liberty(p, q)
                    if num_liberties_of_stone_after_move == 0:
                        num_stones_self_atari = sp.num_of_stones_in_chain(p, q)
                    else:
                        num_stones_self_atari = 0
                # Now update the planes properly
                x.set_capture_size(p, q, num_captured_stones)
                x.set_self_atari_size(p, q, num_stones_self_atari)
                x.set_liberties_after_move(p, q, num_liberties_of_stone_after_move)

        # Debugging code
        # print '\nFor i =', i, "and move =", move
        # for i in range(LIBERTIES_AFTER_MOVE_8 - LIBERTIES_AFTER_MOVE_1 + 1):
        #   print '\n LIBERTIES_AFTER_MOVE_' + str(i + 19) + ': '
        #   x.planes[ LIBERTIES_AFTER_MOVE_1 + i].printPlane()
        # print '\n LIBERTIES_AFTER_MOVE_5: '
        # x.planes[ LIBERTIES_AFTER_MOVE_5].printPlane()

        X.append(x)
        Y.append(y)

    move = moves[-1]
    y = (coord_x, coord_y)
    Y.append(y)

    # write X and y in a file
    if len(X) != len(Y):
        raise Exception('X and Y must have the same number of elements')

    file_counter += 1
    with open('../reduced_dataset/' + str(file_counter) + '.csv', 'w') as f:
        ut.write_header(f)
        for i in range(len(X)):
            X[i].to_file(f) # already finsihes with a comma
            ut.pos_to_array_in_file(Y[i], f)
            f.write('\n')

    break
