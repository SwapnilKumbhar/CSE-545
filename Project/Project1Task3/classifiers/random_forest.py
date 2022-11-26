from sklearn.ensemble import RandomForestClassifier
from . import utils


def run_model(data_tuple):
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(data_tuple[0], data_tuple[2])

    score = utils.get_f1_score(clf, data_tuple)

    print(f"Random forest F1 Score: {score}")
