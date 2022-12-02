from sysdig import (
    runner,
    parser,
)


def get_triples(file_path=None):
    log_file = runner.run_capture() if file_path is None else open(file_path)
    if log_file is None:
        # Logfile error or runner error
        return None
    events = parser.parse_logs(log_file)
    return events
