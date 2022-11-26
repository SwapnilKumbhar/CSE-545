def get_features(implicit_intents: list[str], feature_vector):
    feature_vector.append(len(implicit_intents))
