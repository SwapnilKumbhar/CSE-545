from lxml.etree import _Element


# TODO: Some apps have the same permission multiple times, figure out what to do for the
def get_features(manifest: _Element, feat_vector):
    if manifest is None:
        feat_vector.append(-1)
        return
    permissions = manifest.findall("uses-permission")
    perm_name = "{http://schemas.android.com/apk/res/android}name"

    # Obtained by running `get_top_perms`
    mal_perms = [
        "android.permission.INTERNET",
        "android.permission.READ_PHONE_STATE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.ACCESS_WIFI_STATE",
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.WAKE_LOCK",
        "android.permission.SEND_SMS",
        "android.permission.RECEIVE_SMS",
    ]

    collected_perms = []
    count = 0
    for perm in permissions:
        if perm_name in perm.attrib:
            if perm.attrib[perm_name] in mal_perms:
                if perm.attrib[perm_name] not in collected_perms:
                    count += 1
                    collected_perms.append(perm.attrib[perm_name])

    feat_vector.append(count)
