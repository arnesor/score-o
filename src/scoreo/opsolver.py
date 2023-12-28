"""Module for running opsolver in docker image."""
from pathlib import Path

from python_on_whales import docker

from scoreo.solution import Solution
from scoreo.solution import get_solution


def run_opsolver(problem_file: Path) -> Solution:
    """Run opsolver on the given problem file.

    Args:
        problem_file: The file describing the problem to solve.

    Returns:
        The solution to the problem.
    """
    mnt_dir = problem_file.parent
    docker.run(
        "arneso/opsolver:1",
        ["opt", "--op-exact", "1", f"{str(problem_file.name)}"],
        remove=True,
        volumes=[(str(mnt_dir), "/tmp")],  # nosec B108
    )
    return get_solution(mnt_dir / "stats.json")


def update_distance_limit(problem_file: Path, distance_limit: int) -> None:
    """Update the distance limit in the problem file with the new limit.

    Args:
        problem_file: The file describing the problem to solve.
        distance_limit: The distance limit for the problem, in meters.
    """
    with open(problem_file) as file:
        lines = file.readlines()

    # Iterate through each line and replace the line starting with 'COST_LIMIT : '.
    for i, line in enumerate(lines):
        if line.startswith("COST_LIMIT"):
            lines[i] = f"COST_LIMIT : {distance_limit}\n"

    # Write the updated content back to the file
    with open(problem_file, "w") as file:
        file.writelines(lines)


def find_initial_solution(problem_file: Path) -> Solution:
    """Find initial solution covering all controls.

    Guess an initial distance limit and iterate until the
    shortest cycle covering all controls is found.

    Args:
        problem_file: The file describing the problem to solve.

    Returns:
        The initial solution.
    """
    distance_offset = 10

    # Find a solution containing all controls
    solution = run_opsolver(problem_file)
    while solution.number_of_controls < solution.problem_number_of_controls:
        update_distance_limit(problem_file, solution.distance_limit * 2)
        solution = run_opsolver(problem_file)

    # Find the shortest solution containing all controls
    while solution.number_of_controls == solution.problem_number_of_controls:
        last_solution = solution
        update_distance_limit(problem_file, solution.distance - distance_offset)
        solution = run_opsolver(problem_file)
    return last_solution
