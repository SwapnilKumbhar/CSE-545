"""
Parses the args part of a `read` event

eg. fd=9(<f>/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:2/energy_uj) size=8191
"""


def parse(args: str):
    args = args.split(" ")
    pass
