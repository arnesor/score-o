"""Command-line interface."""
from pathlib import Path

import click
import networkx as nx

from scoreo.course import Course


@click.command()
@click.version_option()
@click.argument("course_file", type=click.Path(exists=True))
def main(course_file: str) -> None:
    """Score Orienteering."""
    course = Course()
    course.read_ocad_course_file(Path(course_file))
    click.echo(f"Read file {click.format_filename(course_file)}")
    print(course)

    g = nx.Graph()

    g.add_edge("A", "C")
    g.add_edge("B", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.add_edge("D", "E")

    nx.draw(
        g,
        with_labels=True,
        node_color="red",
        node_size=3000,
        font_color="white",
        font_size=20,
        font_family="Times New Roman",
        font_weight="bold",
    )
    # plt.show()


if __name__ == "__main__":
    main(prog_name="score-o")  # pragma: no cover
