from lxml.etree import _Element


def get_features(manifest: _Element, feat_vector):
    feat_vector.append(
        len(manifest.findall("uses-permission"))
    ) if manifest is not None else feat_vector.append(-1)
