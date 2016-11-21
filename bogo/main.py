import load as ld
from lasagne import layers
from lasagne.nonlinearities import softmax
from nolearn.lasagne import NeuralNet
import cPickle as pickle
from nolearn.lasagne import BatchIterator

path = '/home/tg/Documents/bogo/converted_database/'

X, Y = ld.load_dataset(folder_path = path, filter_input = True, max_number_states = 10)

_, num_features, size, _ = X.shape

print X.shape
# exit(0)

NUM_FILTERS = 32

net = NeuralNet(
    layers=[
        ('input', layers.InputLayer),
        # ('pad1', layers.shape.PadLayer),
        ('conv1', layers.Conv2DLayer),
        ('conv2', layers.Conv2DLayer),
        ('hidden4', layers.DenseLayer),
        ('output', layers.DenseLayer),
    ],
    input_shape = (None, num_features, size, size),
    conv1_num_filters = NUM_FILTERS,
    conv1_filter_size = (5,5),
    conv2_num_filters = NUM_FILTERS,
    conv2_filter_size = (3,3),
    hidden4_num_units = 1000,
    output_num_units = 361,
    output_nonlinearity = softmax,

    update_learning_rate = 0.5,
    update_momentum = 0.9,

    regression = False, # this is the default?
    batch_iterator_train = BatchIterator(batch_size = 128),
    max_epochs = 30,
    verbose = 1,
    eval_size = 0.2
    )

net.fit(X, Y)
with open('net.pickle', 'wb') as f:
    pickle.dump(net, f, -1)
