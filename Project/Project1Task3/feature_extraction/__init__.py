from glob import glob
from os import path, mkdir

from .core import *
from .core import utils
from asyncio import gather
from logging import getLogger
from time import time
import json

from feature_extraction.features import *

logger = getLogger("FE")


async def extract_features(
    mal_apps_path: str, ben_apps_path: str, regen_data: bool
) -> tuple[list[RawApkData], list[RawApkData]]:
    if not regen_data:
        # Check if we can load from an existing json file
        if not path.exists("mal_data.pkl") or not path.exists("ben_data.pkl"):
            logger.error("Could not find `mal_data.pkl` or `ben_data.pkl`")
            return None, None
        else:
            return utils.deserialize_feats("mal_data.pkl", "ben_data.pkl")

    # Turn paths to absolute
    mal_apps_path = path.abspath(mal_apps_path)
    ben_apps_path = path.abspath(ben_apps_path)

    logger.info(f"Malicious apps path: {mal_apps_path}")
    logger.info(f"Benign apps path:    {ben_apps_path}")

    start_time = time()

    # Create a temporary directory to keep extracted source code
    # This will only happen on the first run for feature extractions
    if not path.exists("extracted_code"):
        mkdir("extracted_code")

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

    utils.serialize_feats(mal_apps_data, ben_apps_data)

    return mal_apps_data, ben_apps_data


def get_feature_matrix(
    mal_apps: list[RawApkData], ben_apps: list[RawApkData], feature_type: int
):
    logger.warn("Extracting features for malicious APKs.")
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
        uses_gps.get_features(mal_app.manifest, feat_vector)
        num_of_write_perms.get_features(mal_app.manifest, feat_vector)
        num_of_access_perms.get_features(mal_app.manifest, feat_vector)
        has_top_mal_perms.get_features(mal_app.manifest, feat_vector)

        if feature_type == 1 or feature_type == 2:
            num_of_implicit_intents.get_features(mal_app.implicit_intents, feat_vector)
            num_of_urls.get_features(mal_app.urls, feat_vector)
            num_of_emails.get_features(mal_app.emails, feat_vector)

        ### Ended calls to all feature extractors

        mal_matrix.append(feat_vector)

    logger.warn(f"Collected {len(mal_matrix)} samples!")

    logger.warn("Extracting features for benign APKs.")
    ben_matrix = []
    for ben_app in ben_apps:
        feat_vector = []

        ### Start calls to all feature extractors

        num_of_perms.get_features(ben_app.manifest, feat_vector)
        intent_filter.get_features(ben_app.manifest, feat_vector)
        has_fine_location.get_features(ben_app.manifest, feat_vector)
        num_of_read_perms.get_features(ben_app.manifest, feat_vector)
        has_coarse_location.get_features(ben_app.manifest, feat_vector)
        uses_camera.get_features(ben_app.manifest, feat_vector)
        uses_gps.get_features(ben_app.manifest, feat_vector)
        num_of_write_perms.get_features(ben_app.manifest, feat_vector)
        num_of_access_perms.get_features(ben_app.manifest, feat_vector)
        has_top_mal_perms.get_features(ben_app.manifest, feat_vector)

        if feature_type == 1 or feature_type == 2:
            num_of_implicit_intents.get_features(ben_app.implicit_intents, feat_vector)
            num_of_urls.get_features(ben_app.urls, feat_vector)
            num_of_emails.get_features(ben_app.emails, feat_vector)

        ### Ended calls to all feature extractors

        ben_matrix.append(feat_vector)

    logger.warn(f"Collected {len(ben_matrix)} samples!")

    return mal_matrix, ben_matrix
