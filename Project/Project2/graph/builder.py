from graph.graph_types import Edge, Node
from sysdig.parser_types import EventData
from sysdig.runner import FORWARD_ACTIONS


def _make(
    evt: EventData,
    subjects: dict[str, Node],
    objects: dict[str, Node],
    edges: list[Edge],
):
    sub = subjects[evt.triple.subject]
    obj = objects[evt.triple.object]

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


def build_graph(evts: list[EventData]):
    edges: list[Edge] = []

    subjects = {}
    objects = {}
    # Create the subjects and objects dict first
    for evt in evts:
        subjects[evt.triple.subject] = Node(
            entity=evt.triple.subject, in_edges=[], out_edges=[]
        )
        objects[evt.triple.object] = Node(
            entity=evt.triple.object, in_edges=[], out_edges=[]
        )

    for evt in evts:
        _make(evt, subjects, objects, edges)
        if not isinstance(evt.triple.subject, str) or not isinstance(
            evt.triple.object, str
        ):
            # We should never reach here.
            print(evt)
            break

    return list(subjects.values()) + list(objects.values()), edges
