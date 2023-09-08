"""Command-line interface."""
from pathlib import Path

import click
import functions
import matplotlib.pyplot as plt
import networkx as nx


@click.command()
@click.version_option()
def main() -> None:
    """Score Orienteering."""
    functions.read_ocad_file(Path("race_230907.Courses.xml"))

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
    plt.show()


if __name__ == "__main__":
    main(prog_name="score-o")  # pragma: no cover
