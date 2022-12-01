from dataclasses import dataclass

# type of FD as a single character.
# Can be 'f' for file, 4 for IPv4 socket, 6 for IPv6 socket, 'u' for unix socket,
# p for pipe, 'e' for eventfd, 's' for signalfd, 'l' for eventpoll, 'i' for inotify,
# 'b' for bpf, 'u' for userfaultd, 'r' for io_uring, 'o' for unknown.

# This is a limited list. We will only look for these types of FDs
FD_CHAR_STR_MAP = {
    "f": "file",
    "4t": "ipv4_socket",
    "6t": "ipv6_socket",
    "4u": "udp4_socket",
    "u": "unix_socket",
}


@dataclass
class LogArgs:
    type: str
    fd_num: int
    data: dict


@dataclass
class NsTime:
    sec: int
    nsec: int

    def __sub__(self, other) -> int:
        sec_diff = self.sec - other.sec
        nsec_diff = self.nsec - other.nsec
        return sec_diff * 1000000000 + nsec_diff

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self == other


@dataclass
class Process:
    path: str
    pid: str


@dataclass
class Triple:
    subject: str
    object: str
    action: str


@dataclass
class EventData:
    event_type: str
    process: Process
    triple: Triple
    start_time: NsTime
    end_time: NsTime
    duration: int
    args: dict
