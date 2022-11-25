from sklearn.svm import SVC
from . import utils


def run_model(data_tuple):
    clf = SVC(gamma="auto")
    clf.fit(data_tuple[0], data_tuple[2])

    score = utils.get_f1_score(clf, data_tuple)

    print(f"F1 Score: {score}")
