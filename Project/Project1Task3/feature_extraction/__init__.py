from glob import glob
from os import path
from .core import *
from asyncio import gather
from logging import getLogger
from time import time

from feature_extraction.features import *

logger = getLogger("FE")


async def extract_features(
    mal_apps_path: str, ben_apps_path: str
) -> tuple[list[RawApkData], list[RawApkData]]:
    # Turn paths to absolute
    mal_apps_path = path.abspath(mal_apps_path)
    ben_apps_path = path.abspath(ben_apps_path)

    logger.info(f"Malicious apps path: {mal_apps_path}")
    logger.info(f"Benign apps path:    {ben_apps_path}")

    start_time = time()
    # Extract raw data
    future_list = []
    for app_path in glob(path.join(mal_apps_path, "*.apk")):
        future_list.append(get_raw_elements(app_path))

    mal_apps_data = await gather(*future_list)
    end_time = time()

    logger.info(f"Gathered! Took {end_time - start_time} seconds")

    start_time = time()
    future_list.clear()
    for app_path in glob(path.join(ben_apps_path, "*.apk")):
        future_list.append(get_raw_elements(app_path))

    ben_apps_data = await gather(*future_list)
    end_time = time()

    logger.info(f"Gathered! Took {end_time - start_time} seconds")

    return mal_apps_data, ben_apps_data


def get_feature_matrix(mal_apps: list[RawApkData], ben_apps: list[RawApkData]):
    mal_matrix = []
    for mal_app in mal_apps:
        feat_vector = []

        ### Start calls to all feature extractors

        num_of_perms.get_features(mal_app.manifest, feat_vector)
        intent_filter.get_features(mal_app.manifest, feat_vector)
        has_fine_location.get_features(mal_app.manifest, feat_vector)
        num_of_read_perms.get_features(mal_app.manifest, feat_vector)
        has_coarse_location.get_features(mal_app.manifest, feat_vector)
        uses_camera.get_features(mal_app.manifest, feat_vector)
        num_of_write_perms.get_features(mal_app.manifest, feat_vector)
        num_of_access_perms.get_features(mal_app.manifest, feat_vector)
        ### Ended calls to all feature extractors

        mal_matrix.append(feat_vector)

    # Remove this
    print(mal_matrix)
