from feature_extraction import *
from feature_extraction.core import *
from classifiers import preprocessor, svc, random_forest, knn
import argparse
import logging
import asyncio


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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
        choices=[1, 2, 3]
    )

    args = parser.parse_args()

    ## Set up logging
    logging.basicConfig(
        format="[%(levelname)s %(name)s]: %(message)s", level=logging.INFO
    )

    mal_app_data, ben_app_data = asyncio.run(
        extract_features(args.malicious, args.benign)
    )

    mal_matrix, ben_matrix = get_feature_matrix(mal_app_data, ben_app_data, args.featuretype)

    """
    data_tuple is a tuple of (x_train, x_test, y_train, y_test)
    xs are data and the ys are label
    """
    data_tuple = preprocessor.prepare_data(mal_matrix, ben_matrix, args.featuretype)
    svc.run_model(data_tuple)
    random_forest.run_model(data_tuple)
    knn.run_model(data_tuple)
