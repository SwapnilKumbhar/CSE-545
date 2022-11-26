from sklearn.neighbors import KNeighborsClassifier
from . import utils


def run_model(data_tuple):
    clf=KNeighborsClassifier(n_neighbors=3)
    clf.fit(data_tuple[0], data_tuple[2])

    score = utils.get_f1_score(clf, data_tuple)

    print(f"K-Nearest Neighbor F1 Score: {score}")