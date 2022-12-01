from sysdig.parser_types import *
from io import TextIOWrapper
import re

from sysdig.runner import BACKWARD_ACTIONS, FORWARD_ACTIONS


FD_TYPE_RE = r"<[\d\w]+>"
FD_STRING_RE = r"fd=\d+\((.*)\)"
EXEC_FILENAME = r"filename=(.*)"


def parse_file_fd(args: str):
    args = args[:-1]  # Remove the last bracket
    args = args[args.find(">") + 1 :]
    return args


def parse_ipv4_fd(args: str):
    args = args[:-1]
    args = args[args.find(">") + 1 :]
    ips = args.split("->")
    src_ip, src_port, dst_ip, dst_port = None, None, None, None
    if len(ips) == 1:
        src_ip, src_port = ips[0].split(":")
    elif len(ips) == 2:
        src_ip, src_port = ips[0].split(":")
        dst_ip, dst_port = ips[1].split(":")

    return {
        "src_ip": src_ip,
        "src_port": src_port,
        "dst_ip": dst_ip,
        "dst_port": dst_port,
    }


def parse_ipv6_fd(args: str):
    return args


def parse_unix_fd(args: str):
    args = args[:-1]
    args = args[args.find(">") + 1 :]
    if len(args) == 0:
        return None
    return args


FD_PARSER_MAP = {
    "unix_socket": parse_unix_fd,
    "file": parse_file_fd,
    "ipv4_socket": parse_ipv4_fd,
    "ipv6_socket": parse_ipv6_fd,
    "udp4_socket": parse_ipv4_fd,
}


def parse_fd(args: str):
    """
    Parses file descriptor and returns a parsed dict

    Eg. fd=5(<4t>192.168.0.18:39622->34.117.59.81:443)
    """
    fd_string_match = re.match(FD_STRING_RE, args)
    if fd_string_match is None:
        return None
    fd_string = fd_string_match.group()
    fd_number = int(fd_string[3])
    fd_type_match = re.search(FD_TYPE_RE, fd_string)
    fd_type = fd_type_match.group()[1:][:-1]

    # Start matching fd_type with its full type
    log_arg = None
    for fd_char, fd_val in FD_CHAR_STR_MAP.items():
        if fd_char in fd_type:
            data = FD_PARSER_MAP[fd_val](fd_string)
            if data is not None:
                # If we get no args, it is impossible to form triples. So we skip.
                log_arg = LogArgs(type=fd_val, fd_num=fd_number, data=data)

                # We have found what we are looking for. Now break.
                break

    fd_string = fd_string[fd_type_match.span()[1] :]

    return log_arg


def parse_filename(args: str):
    if re.search(EXEC_FILENAME, args) is None:
        return None
    else:
        exe = args.split("=")[1]
        return LogArgs(type="program", fd_num=0, data={"exe_path": exe})


PARSER_MAP = {
    "read": parse_fd,
    "readv": parse_fd,
    "write": parse_fd,
    "writev": parse_fd,
    "fcntl": parse_fd,
    "accept": parse_fd,
    "execve": parse_filename,
    "sendmsg": parse_fd,
    "sendto": parse_fd,
    "recvmsg": parse_fd,
    "recvfrom": parse_fd,
}


def make_triples(evt: EventData):
    """
    Creates tuples. Each direction depends on the event type.
    """
    # Events that start from subject and end at object
    if evt.event_type == "execve":
        evt.triple = Triple(
            subject=evt.process.path,
            action=evt.event_type,
            object=evt.args.data["exe_path"],
        )
    elif evt.event_type == "sendmsg":
        obj = evt.args.data["dst_ip"] + ":" + evt.args.data["dst_port"]
        evt.triple = Triple(subject=evt.process.path, action=evt.event_type, object=obj)
    elif evt.event_type == "recvmsg" or evt.event_type == "recvfrom":
        sub = None
        if evt.args.type == "unix_socket":
            sub = evt.args.data
        else:
            sub = (
                evt.args.data["dst_ip"] + ":" + evt.args.data["dst_port"]
                if evt.args.data["dst_ip"] is not None
                else evt.args.data["src_ip"] + ":" + evt.args.data["src_port"]
            )
        evt.triple = Triple(subject=sub, action=evt.event_type, object=evt.process.path)
    else:
        evt.triple = Triple(
            subject=evt.process.path, action=evt.event_type, object=evt.args.data
        )


def parse_logs(log_fd: TextIOWrapper):
    """
    Parses log files generated by `sysdig`
    """
    events: list[EventData] = []
    evt_queue = []
    while True:
        line = log_fd.readline()
        if not line:
            break

        line_vals = line.split("$$")
        if line_vals[2] == ">":
            evt_queue.append(line_vals)
            continue
        else:
            if len(evt_queue) == 0:
                # Something went wrong. We have an event that is exiting but we do not
                # know its entry. We just have to skip this unfortunately.
                continue
            lprev_vals = evt_queue.pop(0)

            start_time = NsTime(*list(map(lambda x: int(x), lprev_vals[1].split("."))))
            end_time = NsTime(*list(map(lambda x: int(x), line_vals[1].split("."))))
            evt = EventData(
                event_type=lprev_vals[5],
                triple=Triple("", "", ""),
                process=Process(lprev_vals[4], lprev_vals[3]),
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                args=PARSER_MAP[lprev_vals[5]](lprev_vals[6]),
            )

            if evt.args is None:
                # Arguments are not there, so we exclude it
                continue

            make_triples(evt)
            events.append(evt)
    # We don't need the file anymore
    log_fd.close()

    # Return this list
    return events