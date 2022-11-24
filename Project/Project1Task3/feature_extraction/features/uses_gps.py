from lxml.etree import _Element


def get_features(manifest: _Element, feat_vector):
    if manifest is None:
        feat_vector.append(-1)
        return

    features = manifest.findall("uses-feature")
    feature_list = [
        "android.hardware.location",
        "android.hardware.location.gps",
        "android.hardware.location.network",
    ]

    feat_name = "{http://schemas.android.com/apk/res/android}name"
    count = 0
    for feature in features:
        if feat_name in feature.keys():
            if feature.attrib[feat_name] in feature_list:
                count += 1

    feat_vector.append(count)
