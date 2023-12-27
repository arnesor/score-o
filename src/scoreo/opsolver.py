"""Module for running opsolver in docker image."""
from pathlib import Path

from python_on_whales import docker


def run_opsolver(problem: Path) -> None:
    """Run opsolver on the given problem file.

    Args:
        problem: The file describing the problem to solve.
    """
    mnt_dir = problem.parent
    output = docker.run(
        "arneso/opsolver:1",
        ["op-solver", "opt", "--op-exact", "1", f"{str(problem.name)}"],
        remove=True,
        volumes=[(str(mnt_dir), "/tmp")],  # nosec B108
    )
    print(output)
