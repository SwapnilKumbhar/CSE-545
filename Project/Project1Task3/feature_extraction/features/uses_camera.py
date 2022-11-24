from lxml.etree import _Element


def get_features(manifest: _Element, feat_vector):
    if manifest is None:
        feat_vector.append(-1)
        return

    features = manifest.findall("uses-feature")

    feat_name = "{http://schemas.android.com/apk/res/android}name"
    for feature in features:
        if feat_name in feature.keys():
            if feature.attrib[feat_name] == "android.hardware.camera":
                feat_vector.append(1)
                return

    feat_vector.append(0)
