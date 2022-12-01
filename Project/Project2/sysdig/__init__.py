from sysdig import (
    runner,
    parser,
)

from pprint import pprint


def get_triples(file_path=None):
    log_file = runner.run_capture() if file_path is None else open(file_path)
    events = parser.parse_logs(log_file)
    return events
