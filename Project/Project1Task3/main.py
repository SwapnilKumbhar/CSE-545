from feature_extraction import *
from feature_extraction.core import *
from classifiers import preprocessor, svc, random_forest, knn
import argparse
import logging
import asyncio
from shutil import which


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Use classification models like SVC, KNN and Random Forest to \
identify malicious applications from the benign ones. \
Depends on `jadx`."""
    )

    parser.add_argument(
        "-b", "--benign", type=str, help="Path to benign apps directory", required=True
    )
    parser.add_argument(
        "-m",
        "--malicious",
        type=str,
        help="Path to malicious apps directory",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--featuretype",
        type=int,
        help="""
Input the type of feature extraction:
[1 - Static features extracted from the manifest file and decompiled Java code,
 2 - Static features extracted from the manifest file and decompiled Java code and preprocessed using PCA (Principle Component Analysis),
 3 - Static features extracted only from the manifest file],
        """,
        required=False,
        default=1,
        choices=[1, 2, 3],
    )
    parser.add_argument(
        "-r",
        "--regen-data",
        help="Regenerate the raw data JSON file by extracting features again from APKs",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--model",
        help="Models to run. Valid values (svc, knn, randomforest). Defaults to 'randomforest'",
        default=["randomforest"],
        choices=["svc", "knn", "randomforest"],
        nargs="+",
    )

    args = parser.parse_args()
    print(args)

    ## Set up logging
    logging.basicConfig(
        format="[%(levelname)s %(name)s]: %(message)s", level=logging.INFO
    )

    logger = logging.getLogger("main")

    # Check if we have `jadx`
    if not which("jadx"):
        logger.error("`jadx` not found. Please install `jadx` to run this program.")
        logger.error("If `jadx` is installed, please ensure that it exists in PATH.")
        exit(-1)

    mal_app_data, ben_app_data = asyncio.run(
        extract_features(args.malicious, args.benign, args.regen_data)
    )

    if (mal_app_data, ben_app_data) == (None, None) and not args.regen_data:
        # Failed to load regen file
        logger.error("Failed to load cached raw data.")

    if (mal_app_data, ben_app_data) == (None, None):
        # This is irrecoverable.
        logger.error("Failed to extract raw features. Exiting...")
        exit(-1)

    mal_matrix, ben_matrix = get_feature_matrix(
        mal_app_data, ben_app_data, args.featuretype
    )

    """
    data_tuple is a tuple of (x_train, x_test, y_train, y_test)
    xs are data and the ys are label
    """
    data_tuple = preprocessor.prepare_data(mal_matrix, ben_matrix, args.featuretype)

    # Run all 3 models
    if "svc" in args.model:
        svc.run_model(data_tuple)
    if "knn" in args.model:
        random_forest.run_model(data_tuple)
    if "randomforest" in args.model:
        knn.run_model(data_tuple)
