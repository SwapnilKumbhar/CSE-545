import sysdig

from graph import builder
from graph.visualize.dot import create_dot
from graph.visualize.image import convert_to_svg

if __name__ == "__main__":
    events = sysdig.get_triples("sysdig_2022_12_01_1669873895.log")
    nodes, edges = builder.build_graph(events)

    dot_file = create_dot(nodes)
    convert_to_svg(dot_file)

    # backtrack(e2)
