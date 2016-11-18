# tries to find, at least, 'min_number' of examples and, at most, 'max_number' of examples
import os
import numpy as np

# constants
SIZE = 19

# methods
def pos_to_coord(pos):
    x, y = pos / SIZE, pos % SIZE

def letter_to_num(c):
    return ord(c) - 97

# main
states = np.zeros((SIZE, SIZE))

folder = os.getcwd()

with open('_nfolds_database.data', 'a') as g:
    for fname in sorted(os.listdir(folder)):
        if fname.endswith('.sgf'):
            with open(fname, 'r') as f:
                text = "".join([line.strip() for line in f.readlines()])
                text = text[1:-1] # remove parenthesis
                moves = text.split(';')[2:] # remove metadata
                for move in moves:
                    if len(move) != 5:
                        print fname, move
                    else:
                        _, _, x, y, _ = move
                        x, y = letter_to_num(x), letter_to_num(y)
                        if x < 0 or y < 0 or x >= SIZE or y >= SIZE:
                            print fname, x, y
                        else:
                            states[x][y] += 1

print states
print states.sum()
print states.sum()*8
