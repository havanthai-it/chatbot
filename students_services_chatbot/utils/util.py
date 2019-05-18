import numpy as np
import pickle

from random import shuffle


def softmax_to_one_hot(X):
    """
    Convert from softmax matrix to one hot matrix
    Return (X one hot, max probability)
    """
    X_oh = np.zeros(X.shape)
    max_proba = np.zeros((X.shape[0], 1))
    max_index = np.argmax(X, axis=1)
    for i in range(len(X)):
        X_oh[i][max_index[i]] = 1
        max_proba[i][0] = X[i][max_index[i]]
    return X_oh, max_proba


def pickle_save_object(object, path):
    """Save an object with pickle"""
    pickle_writer = open(path, "wb")
    pickle.dump(object, pickle_writer)
    pickle_writer.close()


def pickle_load_object(path):
    """Load an object with pickle"""
    pickle_reader = open(path, "rb")
    result = pickle.load(pickle_reader)
    pickle_reader.close()
    return result


def shuffle_matrix(X, y):
    """Shuffle X, y"""
    m = len(X)
    shuffle_indexes = [i for i in range(m)]
    shuffle(shuffle_indexes)

    X_shuffled = []
    y_shuffled = []
    for i in range(m):
        X_shuffled.append(X[shuffle_indexes[i]])
        y_shuffled.append(y[shuffle_indexes[i]])

    return np.array(X_shuffled), np.array(y_shuffled)
