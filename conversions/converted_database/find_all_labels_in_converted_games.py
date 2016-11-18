# tries to find, at least, 'min_number' of examples and, at most, 'max_number' of examples
import os
import numpy as np

# constants
SIZE = 19

# methods
def pos_to_coord(pos):
    x, y = pos % SIZE

# main
folder = os.getcwd()

states = np.zeros(SIZE * SIZE)

with open('_nfolds_database.data', 'a') as g:
    for fname in sorted(os.listdir(folder)):
        if fname.endswith('.data'):
            with open(fname, 'r') as f:
                f.readline() # header
                for line in f:
                    pos = int(line.strip().split(',')[-1])
                    states[pos] += 1

print states
