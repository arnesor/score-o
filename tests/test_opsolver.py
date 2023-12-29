from pathlib import Path

import pytest

from scoreo.opsolver import find_all_solutions
from scoreo.opsolver import find_initial_solution
from scoreo.opsolver import run_opsolver


@pytest.fixture()
def problem_file(tmp_path: Path) -> Path:
    """Copy the test problem file to a temporary directory."""
    source = Path(__file__).parent / "data" / "race_230907-5016.oplib"
    destination = tmp_path / source.name
    destination.write_bytes(source.read_bytes())
    return destination


def test_run_opsolver(problem_file: Path) -> None:
    solution = run_opsolver(problem_file)
    assert solution.number_of_controls == 25
    assert solution.score == 335
    assert solution.distance == 4875


def test_find_initial_solution(problem_file: Path) -> None:
    solution = find_initial_solution(problem_file)
    assert solution.number_of_controls == 26
    assert solution.score == 340


def test_find_all_solutions(problem_file: Path) -> None:
    solutions = find_all_solutions(problem_file, 5200, 4800)
    assert solutions[0].number_of_controls == 26


if __name__ == "__main__":
    source = Path(__file__).parent / "data" / "race_230907" / "race_230907-5016.oplib"
    test_find_all_solutions(source)
