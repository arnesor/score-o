"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Score Orienteering."""


if __name__ == "__main__":
    main(prog_name="score-o")  # pragma: no cover
