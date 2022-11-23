from feature_extraction import extract_features
from feature_extraction.core import *
import argparse
import logging
import asyncio


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--benign", type=str, help="Path to benign apps directory"
    )
    parser.add_argument(
        "-m", "--malicious", type=str, help="Path to malicious apps directory"
    )

    args = parser.parse_args()

    ## Set up logging
    logging.basicConfig(
        format="[%(levelname)s %(name)s]: %(message)s", level=logging.INFO
    )

    mal_app_data, ben_app_data = asyncio.run(
        extract_features(args.malicious, args.benign)
    )
