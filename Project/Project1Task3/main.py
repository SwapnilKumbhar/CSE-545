from feature_extraction import *
from feature_extraction.core import *
from classifiers import preprocessor, svc
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

    args = parser.parse_args()

    ## Set up logging
    logging.basicConfig(
        format="[%(levelname)s %(name)s]: %(message)s", level=logging.WARN
    )

    mal_app_data, ben_app_data = asyncio.run(
        extract_features(args.malicious, args.benign)
    )

    mal_matrix, ben_matrix = get_feature_matrix(mal_app_data, ben_app_data)

    """
    data_tuple is a tuple of (x_train, x_test, y_train, y_test)
    xs are data and the ys are label
    """
    data_tuple = preprocessor.prepare_data(mal_matrix, ben_matrix)
    svc.run_model(data_tuple)
