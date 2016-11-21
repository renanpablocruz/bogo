import cPickle as pickle
from nolearn.lasagne import NeuralNet
import numpy as np
import matplotlib.pyplot as pyplot

def load_net(fname):
	return pickle.load(open(fname, 'rb'))

net = load_net('net.pickle')

train_loss = np.array([i["train_loss"] for i in net.train_history_])
valid_loss = np.array([i["valid_loss"] for i in net.train_history_])
pyplot.plot(train_loss[1:], linewidth=3, label="train")
pyplot.plot(valid_loss[1:], linewidth=3, label="valid")
pyplot.grid()
pyplot.legend()
pyplot.xlabel("epoch")
pyplot.ylabel("loss")
# pyplot.ylim(1e-3, 1e-2)
pyplot.yscale("log")
pyplot.show()
