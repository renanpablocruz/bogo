import os
import numpy as np
from pandas.io.parsers import read_csv
from sklearn.utils import shuffle
import utils as ut
import copy
import math

SIZE = 19

# def load(fname):
#     with open(fname, 'r') as f:
#         header = f.readline()
#         all_features = []
#         targets = []
#         for line in f:
#             l = map(lambda x: map(int, x.split(' ')), line.strip().split(','))
#             features = l[:-1]
#             target = l[-1]
#             all_features.append(features)
#             targets.append(target)

#     size = int(math.sqrt(len(all_features[0][0])))
#     num_features = len(all_features[0])

#     X = np.vstack(all_features)
#     X = X.reshape(-1, num_features, size, size)
#     Y = np.vstack(targets)
#     X, Y = shuffle(X, Y) # could include random_state=a_number parameter for reproducibility
#     X = X.astype(np.float32)
#     Y = Y.astype(np.float32)
#     return X, Y

def load(fname, all_features, targets, filter_input, max_number_states, state_counter):
    with open(fname, 'r') as f:
        header = f.readline()
        for line in f:
            l = map(lambda x: map(int, x.split(' ')), line.strip().split(','))
            features = l[:-1]
            target = l[-1][0]
            # print 'target', target
            # exit(0)
            if not filter_input:
                all_features.append(features)
                targets.append(target)
            elif state_counter[target] < max_number_states:
                all_features.append(features)
                targets.append(target)
                state_counter[target] += 1

def load_dataset(folder_path, filter_input = False, max_number_states = 10):
    if filter_input:
        state_counter = np.zeros(SIZE * SIZE)
    else:
        state_counter = None

    all_features = []
    targets = []

    # for fname in sorted(os.listdir(folder_path)):
    for fname in os.listdir(folder_path):
        if fname.endswith('.data'):
            load(folder_path + fname, all_features, targets, filter_input, max_number_states, state_counter)

    size = int(math.sqrt(len(all_features[0][0])))
    num_features = len(all_features[0])

    X = np.vstack(all_features)
    X = X.reshape(-1, num_features, size, size)
    Y = np.array(targets)
    X, Y = shuffle(X, Y) # could include random_state=a_number parameter for reproducibility
    X = X.astype(np.float32)
    Y = Y.astype(np.int32)
    # print 'Y'
    # print Y
    # exit(0)
    return X, Y