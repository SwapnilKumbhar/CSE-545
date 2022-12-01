from graph.graph_types import Edge, Node
from graph.visualize import dot
from graph.visualize import image


NODES_SET = set()
NODES_SET_FILTERED = set()


def backtrack(poi: Edge):
    global NODES_SET
    global NODES_SET_FILTERED

    to_node: Node = poi.end_node
    to_node.in_edges = [poi]
    to_node.out_edges = []

    NODES_SET.add(to_node)
    NODES_SET_FILTERED.add(to_node)

    backtrack_recurse(poi)
    nodes = list(NODES_SET)

    dot_file = dot.create_dot(nodes, "backtracked")
    image.convert_to_svg(dot_file)

    filter_edges(poi)
    nodes = list(NODES_SET_FILTERED)

    dot_file = dot.create_dot(nodes, "filtered")
    image.convert_to_svg(dot_file)


def backtrack_recurse(poi: Edge):
    global NODES_SET

    from_node: Node = poi.from_node

    node = from_node
    node.out_edges = []

    if node not in NODES_SET:
        NODES_SET.add(node)

        for in_edge in from_node.in_edges:
            backtrack_recurse(in_edge)


def filter_edges(poi: Edge):
    global NODES_SET_FILTERED

    from_node: Node = poi.from_node

    old_in_edges = from_node.in_edges
    node = from_node
    node.out_edges = []

    # Clear out all in edges initially, in the loop, we only add in edges that satisfy trackability condition
    node.in_edges = []

    in_edges = []

    if node not in NODES_SET_FILTERED:
        NODES_SET_FILTERED.add(node)

        for in_edge in old_in_edges:
            if in_edge.start_time < poi.end_time:
                in_edges.append(in_edge)
                filter_edges(in_edge)

        node.in_edges = in_edges
