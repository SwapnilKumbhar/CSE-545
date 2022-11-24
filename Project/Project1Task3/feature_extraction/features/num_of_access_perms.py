from lxml import etree

from lxml.etree import _Element

ANDROID_NAME = "{http://schemas.android.com/apk/res/android}name"
ACCESS_PERM = "android.permission.ACCESS"

def get_features(manifest: _Element, feature_vector):

    if manifest is None:
        feature_vector.append(-1)
        return

    perms = manifest.findall("uses-permission")

    read_perms = 0

    for perm in perms:
        if ANDROID_NAME in perm.attrib.keys() and perm.attrib[ANDROID_NAME].startswith(ACCESS_PERM):
            read_perms += 1

    feature_vector.append(read_perms)
