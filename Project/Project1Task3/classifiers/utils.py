from sklearn.metrics import f1_score


def get_f1_score(clf, data_tuple):
    y_pred = clf.predict(data_tuple[1])
    return f1_score(data_tuple[3], y_pred)
