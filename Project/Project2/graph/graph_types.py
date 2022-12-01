from dataclasses import dataclass
from sysdig.parser_types import NsTime


@dataclass
class Edge:
    from_node = None  # :Node
    end_node = None  # :Node
    action: str
    start_time: NsTime
    end_time: NsTime

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self == other


@dataclass
class Node:
    entity: str
    in_edges: list[Edge]
    out_edges: list[Edge]

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self == other
