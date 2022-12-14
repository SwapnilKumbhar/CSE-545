from lxml.etree import _Element


def get_features(manifest: _Element, feat_vector):
    if manifest is None:
        feat_vector.append(-1)
        return
    permissions = manifest.findall("uses-permission")
    perm_name = "{http://schemas.android.com/apk/res/android}name"
    for perm in permissions:
        if perm_name in perm.attrib:
            if perm.attrib[perm_name] == "android.permission.ACCESS_COARSE_LOCATION":
                feat_vector.append(1)
                return

    feat_vector.append(0)
