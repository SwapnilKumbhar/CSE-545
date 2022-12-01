import subprocess


def convert_to_svg(dot_file: str):

    # Create svg file to view the graph as an image
    cmd = ["dot", "-Tsvg", dot_file]
    svg_file = open("output.svg", "w")
    p = subprocess.Popen(cmd, stdout=svg_file, stderr=subprocess.PIPE)
    p.wait()
