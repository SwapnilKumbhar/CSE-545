from dataclasses import dataclass
from sysdig.parser_types import NsTime
from typing import List


@dataclass
class Edge:
    from_node: object  # :Node
    end_node: object  # :Node
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
    id: str
    in_edges: List[Edge]
    out_edges: List[Edge]

    def __hash__(self):
        return hash(self.entity)

    def __eq__(self, other):
        return self == other
