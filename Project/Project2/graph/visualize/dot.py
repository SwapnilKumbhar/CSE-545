from graph.graph_types import Node
from graphviz import Digraph


def create_dot(nodes: list[Node]) -> str:
    dot = Digraph(format="dot")

    # Add nodes and store node is to name mapping in a dict for creating edges later
    node_names_dict = {}

    for index, node in enumerate(nodes):
        node_name = f"n{index + 1}"
        node_label = node.entity
        dot.node(node_name, node_label)

        node_names_dict[node] = node_name

    # Iterate through all edges of every node (only in_edges is enough)
    for node in nodes:
        for edge in node.in_edges:
            from_node_name = node_names_dict[edge.from_node]
            end_node_name = node_names_dict[edge.end_node]
            dot.edge(from_node_name, end_node_name)

    # Save dot file and return the file name
    file_name = "output"
    dot.render(filename=file_name)

    return f"{file_name}.dot"
