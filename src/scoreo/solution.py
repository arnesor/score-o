"""Functions for working with the solutions from opsolver."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Solution:
    """Class for storing information about a solution."""

    score: int
    number_of_controls: int
    distance: int
    controls: list[int]
    distance_limit: int
    problem_number_of_controls: int


def get_last_solution(solution_file: Path) -> Solution:
    """Check and extract information from the solution generated by opsolver."""
    with open(solution_file) as file:
        last_line = file.readlines()[-1]
    last_sol = json.loads(last_line)

    return Solution(
        last_sol["sol"]["val"],
        last_sol["sol"]["sol_ns"],
        last_sol["sol"]["cap"],
        last_sol["sol"]["cycle"],
        last_sol["prob"]["d0"],
        last_sol["prob"]["n"],
    )


def get_all_solutions(solution_file: Path) -> list[Solution]:
    """Check and extract information from all solutions generated by opsolver."""
    solutions = []
    with open(solution_file) as file:
        lines = file.readlines()

    for line in lines:
        sol_json = json.loads(line)
        solutions.append(
            Solution(
                sol_json["sol"]["val"],
                sol_json["sol"]["sol_ns"],
                sol_json["sol"]["cap"],
                sol_json["sol"]["cycle"],
                sol_json["prob"]["d0"],
                sol_json["prob"]["n"],
            )
        )

    return solutions
