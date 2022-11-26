"""
Utility for splitting training-testing data, applying PCA, etc.
"""
import numpy as np
from sklearn.model_selection import train_test_split

# Total features = 13 but consider only first 8 important features if feature type is given as 2
PRINCIPAL_FEATURES = 8


def prepare_data(mal_matrix, ben_matrix, feature_type):
    labels = np.append(np.repeat(1, len(mal_matrix)), np.repeat(0, len(ben_matrix)))

    features = np.append(np.array(mal_matrix), np.array(ben_matrix), axis=0)

    if feature_type == 2:
        features = PCA(features)

    return train_test_split(features, labels, test_size=0.2)


def PCA(features):

    # Apply principal  component analysis
    features_meaned = features - np.mean(features , axis = 0)
    cov_mat = np.cov(features_meaned , rowvar = False)
    eigen_values , eigen_vectors = np.linalg.eigh(cov_mat)
    sorted_index = np.argsort(eigen_values)[::-1]
    sorted_eigenvectors = eigen_vectors[:,sorted_index]

    # Get only the top 'PRINCIPAL_FEATURES' number of features
    eigenvector_subset = sorted_eigenvectors[:,0:PRINCIPAL_FEATURES]
    features_reduced = np.dot(eigenvector_subset.transpose(), features_meaned.transpose()).transpose()
    
    return features_reduced
