from lxml.etree import _Element


def get_features(manifest: _Element, feat_vector):
    if manifest is None:
        feat_vector.append(-1)
        return
    permissions = manifest.findall("uses-permission")
    for perm in permissions:
        if (
            perm.attrib["{http://schemas.android.com/apk/res/android}name"]
            == "android.permission.ACCESS_FINE_LOCATION"
        ):
            feat_vector.append(1)
            return

    feat_vector.append(0)
