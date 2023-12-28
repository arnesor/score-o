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


def find_initial_solution(problem_file: Path) -> Solution:
    """Find initial solution covering all controls.

    Guess an initial distance limit and iterate until the
    shortest cycle covering all controls is found.

    Args:
        problem_file: The file describing the problem to solve.

    Returns:
        The initial solution.
    """
    return Solution(0, 0, 0, 0, [])
