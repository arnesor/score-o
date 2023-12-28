"""Command-line interface."""
from pathlib import Path

import click

from scoreo.course import Course


@click.command()
@click.version_option()
@click.argument("course_file", type=click.Path(exists=True))
def main(course_file: str) -> None:
    """Score Orienteering."""
    filename = Path(course_file)
    basename = filename.stem.split(".")[0]
    score_file = filename.parent / f"{basename}.sco"

    course = Course()
    course.read_ocad_course_file(filename)
    click.echo(f"Read file {click.format_filename(course_file)}")

    if score_file.is_file():
        course.read_score_file(score_file)
        course.write_opsolver_file(filename, course.estimate_max_distance())
    else:
        click.echo(f"No score file: {score_file} Creating template. Fill in and rerun.")
        course.write_score_template(score_file)

    # print(course)


if __name__ == "__main__":
    main(prog_name="score-o")  # pragma: no cover
