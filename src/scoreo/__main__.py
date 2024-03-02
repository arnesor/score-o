"""Command-line interface."""

from pathlib import Path

import click

from scoreo.course import Course
from scoreo.opsolver import find_all_solutions
from scoreo.opsolver import find_initial_solution


@click.command()
@click.version_option()
@click.argument("course_file", type=click.Path(exists=True))
@click.option(
    "--start", type=int, help="Start distance, the distance to start the search at."
)
@click.option(
    "--stop", type=int, help="Stop distance, the distance to stop the search at."
)
@click.option(
    "--heuristic", is_flag=True, default=False, help="Enable or disable heuristic mode."
)
def main(
    course_file: str, start: int | None, stop: int | None, heuristic: bool
) -> None:
    """Score Orienteering."""
    filename = Path(course_file)
    basename = filename.stem.split(".")[0]
    score_file = filename.parent / f"{basename}.sco"

    course = Course()
    course.read_ocad_course_file(filename)
    click.echo(f"Read file {click.format_filename(course_file)}")

    if score_file.is_file():
        distance_limit = course.estimate_max_distance() if start is None else start
        stop_distance = course.get_stop_distance() if stop is None else stop
        course.read_score_file(score_file)
        problem_file = course.write_opsolver_file(filename, distance_limit)
        if start is None:
            initial_solution = find_initial_solution(problem_file)
            solutions = find_all_solutions(
                problem_file, initial_solution.distance_limit, stop_distance, heuristic
            )
        else:
            solutions = find_all_solutions(
                problem_file, distance_limit, stop_distance, heuristic
            )
        click.echo("Found solutions:")
        for solution in solutions:
            click.echo(solution)
    else:
        click.echo(f"No score file: {score_file} Creating template. Fill in and rerun.")
        course.write_score_template(score_file)


if __name__ == "__main__":
    main(prog_name="score-o")  # pragma: no cover
