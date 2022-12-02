from graph.graph_types import Edge, Node
from sysdig.parser_types import EventData
from sysdig.runner import FORWARD_ACTIONS
from typing import Dict, List
from loguru import logger


def _make(
    evt: EventData,
    nodes: Dict[str, Node],
    edges: List[Edge],
):
    sub = nodes[evt.triple.subject]
    obj = nodes[evt.triple.object]

    # set direction
    if evt.triple.action in FORWARD_ACTIONS:
        e = Edge(
            from_node=sub,
            end_node=obj,
            action=evt.triple.action,
            start_time=evt.start_time,
            end_time=evt.end_time,
        )
        sub.out_edges.append(e)
        obj.in_edges.append(e)
        edges.append(e)
    else:
        e = Edge(
            from_node=obj,
            end_node=sub,
            action=evt.triple.action,
            start_time=evt.start_time,
            end_time=evt.end_time,
        )
        sub.in_edges.append(e)
        obj.out_edges.append(e)
        edges.append(e)


def build_graph(evts: List[EventData]):
    edges: List[Edge] = []

    nodes = {}
    # Create the subjects and objects dict first
    for evt in evts:
        if evt.triple.subject not in nodes:
            nodes[evt.triple.subject] = Node(
                id=evt.event_id, entity=evt.triple.subject, in_edges=[], out_edges=[]
            )
        if evt.triple.object not in nodes:
            nodes[evt.triple.object] = Node(
                id=evt.event_id, entity=evt.triple.object, in_edges=[], out_edges=[]
            )

    logger.info(f"Total entities: {len(nodes.keys())}")

    for evt in evts:
        _make(evt, nodes, edges)
        if not isinstance(evt.triple.subject, str) or not isinstance(
            evt.triple.object, str
        ):
            # We should never reach here.
            print(evt)
            break

    return nodes.values(), edges
