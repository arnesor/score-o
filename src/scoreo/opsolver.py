"""Module for running opsolver in docker image."""

from pathlib import Path

from python_on_whales import docker

from scoreo.solution import Solution
from scoreo.solution import get_last_solution


def run_opsolver(problem_file: Path, heuristic: bool = False) -> Solution:
    """Run opsolver on the given problem file.

    Args:
        problem_file: The file describing the problem to solve.
        heuristic: Whether to use heuristic algorithm or not. Defaults to False.

    Returns:
        The solution to the problem.
    """
    mnt_dir = problem_file.parent
    exact = str(int(heuristic is False))
    docker.run(
        "arneso/opsolver:1",
        ["opt", "--op-exact", f"{exact}", f"{str(problem_file.name)}"],
        remove=True,
        volumes=[(str(mnt_dir.resolve()), "/tmp")],  # nosec B108
    )
    return get_last_solution(mnt_dir / "stats.json")


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
    last_solution = solution
    while solution.number_of_controls == solution.problem_number_of_controls:
        last_solution = solution
        update_distance_limit(problem_file, solution.distance - distance_offset)
        solution = run_opsolver(problem_file)
    return last_solution


def find_all_solutions(
    problem_file: Path, start_distance: int, stop_distance: int, heuristic: bool = False
) -> list[Solution]:
    """Find all solutions shorter than the distance limit.

    Start at distance limit and generate solutions iteratively with shorter limits.

    Args:
        problem_file: The file describing the problem to solve.
        start_distance: The distance limit for the problem, in meters.
        stop_distance: Finish the search when this distance is reached.
        heuristic: Whether to use heuristic algorithm or not. Defaults to False.

    Returns:
        A list of solutions.
    """
    distance_offset = 10

    solutions = []
    update_distance_limit(problem_file, start_distance)
    solution = run_opsolver(problem_file)
    i = 1
    print(f"Iteration {i}: {solution}")
    while solution.distance > stop_distance:
        solutions.append(solution)
        update_distance_limit(problem_file, solution.distance - distance_offset)
        solution = run_opsolver(problem_file)
        i += 1
        print(f"Iteration {i}: {solution}")

    solutions.append(solution)

    return solutions
