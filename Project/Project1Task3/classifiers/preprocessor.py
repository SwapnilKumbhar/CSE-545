"""
Utility for splitting training-testing data, applying PCA, etc.
"""
import numpy as np
from sklearn.model_selection import train_test_split


def prepare_data(mal_matrix, ben_matrix):
    labels = np.append(np.repeat(1, len(mal_matrix)), np.repeat(0, len(ben_matrix)))

    data = np.append(np.array(mal_matrix), np.array(ben_matrix), axis=0)

    return train_test_split(data, labels, test_size=0.2)
