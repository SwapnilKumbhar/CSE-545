from graph.graph_types import Node, Edge
from graph.visualize.dot import create_dot
from graph.visualize.image import convert_to_svg
from graph.backtracker import backtrack

if __name__ == "__main__":
    e1 = Edge("execve", 3.023, 5.138)
    e2 = Edge("read", 5.129, 7.283)
    e3 = Edge("recvmsg", 2.172, 8.811)
    e4 = Edge("sendmsg", 3.626, 7.387)

    n1 = Node("/usr/bin/node1", [e4], [e1, e2])
    n2 = Node("/usr/bin/node2", [e1, e3], [])
    n3 = Node("/usr/bin/node3", [e2], [])
    n4 = Node("/usr/bin/node4", [], [e3, e4])

    e1.from_node = n1
    e1.end_node = n2

    e2.from_node = n1
    e2.end_node = n3

    e3.from_node = n4
    e3.end_node = n2

    e4.from_node = n4
    e4.end_node = n1

    nodes = [n1, n2, n3, n4]

    dot_file = create_dot(nodes)
    convert_to_svg(dot_file)

    backtrack(e2)
