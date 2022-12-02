from loguru import logger
import sysdig
from sysdig import runner
from graph import builder
from graph.visualize.dot import create_dot, dot_exists
from graph.visualize.image import convert_to_svg
from graph.backtracker import backtrack

import argparse
from os import path
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualize sysdig output and filter based on Points of Interest. Depends on `dot` and `sysdig`"
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        required=False,
        help="Optional sysdig input. If not given, the script will run `sysdig` and generate this file in real-time.",
    )

    args = parser.parse_args()
    # Setup logging
    logger.remove(0)
    logger.level("INFO", color="<cyan>")
    logger.add(
        sys.stdout,
        format="<level>[{level}][{module}] {message}</level>",
        colorize=True,
    )
    logger.info("Starting!")

    # Check if required executables are available
    if not dot_exists():
        logger.error("Could not find `dot`. Please install it.")
        exit(-1)

    events = {}
    if args.file is not None:
        # Check if the file exists
        if path.exists(args.file):
            events = sysdig.get_triples(args.file)
        else:
            if not runner.sysdig_exists():
                logger.error("Could not find `sysdig`. Please install it.")
                exit(-1)
    else:
        events = sysdig.get_triples()

    # Show triples result
    logger.info("Printing found triples --")
    for event in events:
        logger.info(event.triple)

    if events is None:
        # Something went wrong
        logger.error("Could not parse events. Exiting...")
        exit(-1)
    nodes, edges = builder.build_graph(events)

    dot_file = create_dot(nodes)
    convert_to_svg(dot_file)

    logger.info("Searching for POI edge")

    poi = list(
        filter(
            lambda e: e.end_node.entity == "/usr/bin/cat" and e.action == "execve",
            edges,
        )
    )[0]

    backtrack(poi)
