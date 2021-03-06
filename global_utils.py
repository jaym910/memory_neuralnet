import numpy as np
from scipy.special import expit
import pickle

"""Global utility methods.
"""
PHONEME_MAPPING = None
BECNHMARK_PER = 50 # benchmarks at every 50 epoch

def load_phoneme_mapping():
    global PHONEME_MAPPING
    f = file('datasets/phonemeslabel.csv', 'r')
    line = f.readline()
    labels = [c.rsplit()[0] for c in line.split(',')]
    f1 = file('datasets/phonemespat.csv', 'r')
    data_vectors = [np.matrix(map(int, line.rstrip().split(","))) for line in f1]
    phoneme_mapping = {}
    for i, l in enumerate(labels):
        phoneme_mapping[l] = data_vectors[i]

    PHONEME_MAPPING = phoneme_mapping
    return phoneme_mapping


def most_similar_phoneme_l2(input_vector, phoneme_mapping):
    """ Get most similar phenome vector to input vector
    similarity = l2 norm
    """
    min_diff = len(input_vector)
    most_sim = None
    for key in phoneme_mapping:
        p = phoneme_mapping[key]
        if (p.T == input_vector).all():
            return key
        squares = np.power(input_vector-p.T, 2)
        diff = np.sqrt(np.sum(squares))
        if diff <= min_diff:
            min_diff = diff
            most_sim = key
    return most_sim


def most_similar_phoneme_l1(input_vector, phoneme_mapping):
    """ Get most similar phenome vector to input vector
    similarity = l1 norm
    """
    min_diff = len(input_vector)
    most_sim = None
    for key in phoneme_mapping:
        p = phoneme_mapping[key]
        if (p.T == input_vector).all():
            return key
        diff = input_vector-p.T
        diff = np.sum(np.abs(diff))
        if diff <= min_diff:
            min_diff = diff
            most_sim = key
    return most_sim


def string_to_vector(s):
    """Convert a string to concatenated 1-of-26 vectors.

    -Jay
    """
    indices = [ord(x)-97 for x in s]
    vector = np.zeros(len(s)*26)
    vector[np.arange(0, 26*len(s), 26)+indices] = 1
    return vector


def sigmoid(x):
    """Sigmoid activation function. Works on scalars, vectors, matrices."""
    return expit(x)
    # return 1.0 / (1.0+np.exp(-1.0*x))


def logit(x):
    """Logit function (inverse of sigmoid).
    Works on scalars, vectors, matrices."""
    return np.log(x/(1-x))


def id(x):
    """Identity (linear) activatione."""
    return x


def cross_entropy(output, target):
    """Get cross entropy between ouput and desired target"""
    output = np.array(output)
    target = np.array(target)
    s = -1.0/float(len(output))
    return s*np.sum(target*np.log(output)+(1-target)*np.log(1-output))


def sum_of_squares_error(output, target):
    """Sum of squares error function"""
    return .5*np.sum(np.power(np.subtract(output,target),2))


def last_seen(m):
    """Grab the last memory.

    Since we store memories before the output processes them,
    we actually want to grab the second to last memory in the list.
    Since python lists are inherently circular, on the first run through,
    when there's only 1 memory, it will grab the memory of itself.
    """

    memory_weight = .1  # how much do we weight the last memory by?
    mem = m.memory_array[-2]  # grab second to last memory
    return mem*memory_weight


def store_every(I_activ, m, error=None):
    """Store any memory, no deletion or anything."""

    # make sure not going over memory limit
    # if so remove the oldest one

    if len(m.memory_array) == m.limit:
        m.memory_array = m.memory_array[1:]

    m.memory_array.append(I_activ)


def load_data(data_set):
    """Load data_set

    Args:
        data_set: file name (string)
    Returns:
        two lists of vectors: inputpatterns, outputpatterns
    """
    f = open(data_set)
    ipats = []
    tpats = []
    for line in f.readlines():
        items = line.split()
        ipat = string_to_vector(items[0])
        tup = items[-1]
        tpat = np.array([int(tup[1]), int(tup[3])])
        ipats.append(ipat)
        tpats.append(tpat)
    return ipats, tpats


def save_net(name, network):
    pickle.dump(network, open(str(name), "wb"))


def load_net(name):
    return pickle.load(file(str(name), 'rb'))


if __name__ == "__main__":
    m = load_phoneme_mapping()
    v = np.matrix(
                  np.random.randint(2, size=(16, 1)))
    print most_similar_phoneme_l2(v, m)



