"""
Wrapper around the `sysdig` utility
"""
from shutil import which
from loguru import logger
import subprocess
import os
from datetime import datetime

sysdig_exists = lambda: which("sysdig") is not None

is_root = lambda: os.geteuid() == 0

# Event attributes to get, in this order
EVT_ATTRS = [
    "%evt.num",
    "%evt.rawtime.s.%evt.rawtime.ns",
    "%evt.dir",
    "%proc.pid",
    "%proc.exepath",
    "%evt.type",
    "%evt.args",
    "%proc.name",
]

# Processes to filter out
PROC_FILTER = [
    "sysdig",
    "sshd",
    "irqbalance",
    "accounts-daemon",
    "thermald",
    "systemd-journal",
    "systemd-udev",
    "systemd-resolve",
    "snapd",
    "gmain",
    "systemd",
]

# Events to look for
EVT_FILTER = [
    "read",
    "readv",
    "write",
    "writev",
    "fcntl",
    "accept",
    "execve",
    # Clone is being a little complicated with logs for now.
    # "clone",
    "sendmsg",
    "sendto",
    "recvmsg",
    "recvfrom",
]

# Events where information flows from subject to object
FORWARD_ACTIONS = {"write", "writev", "fcntl", "execve", "sendmsg", "sendto"}

# Events where information flows from object to subject
BACKWARD_ACTIONS = {"read", "readv", "recvmsg", "recvfrom"}


# Name of the logfile that will hold `sysdig` data
SYSDIG_LOG_FILE_NAME = f"sysdig_{datetime.now().strftime('%Y_%m_%d_%s')}.log"


def run_capture():
    """
    Runs the `sysdig` utility, saves output to a file. Then, returns the file object
    of the file that contains the `sysdig` output
    """

    # Basic checks
    if not sysdig_exists():
        logger.error("`sysdig` does not exist. Please install `sysdig`")
        return None

    if not is_root():
        logger.error(
            "Please run this script as `root`. `sysdig` needs superuser permissions."
        )
        return None

    # Construct filters and format
    proc_filter = " and ".join(list(map(lambda p: f"proc.name!={p}", PROC_FILTER)))
    evt_filter = " or ".join(list(map(lambda e: f"evt.type={e}", EVT_FILTER)))

    format = "$$".join(EVT_ATTRS)
    filter = f"({proc_filter}) and ({evt_filter})"

    args = ["sysdig", "-p", format, filter]

    log_file = open(SYSDIG_LOG_FILE_NAME, "w+")
    # We are choosing enter but any key is ok.
    input("Press ENTER to start `sysdig` capture: ")
    proc = subprocess.Popen(args, stdout=log_file)
    print(f"Started capture! Saving data to {SYSDIG_LOG_FILE_NAME}")
    input("Press ENTER to stop `sysdig` capture: ")
    print("\n")
    # Kill process
    proc.kill()

    # reset seeker to 0
    log_file.seek(0)
    return log_file
