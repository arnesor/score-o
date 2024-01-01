from pathlib import Path

from scoreo.solution import get_all_solutions
from scoreo.solution import get_last_solution


def test_get_last_solution() -> None:
    filename = Path(__file__).parent / "data" / "stats.json"
    solution = get_last_solution(filename)
    assert solution.number_of_controls == 25
    assert solution.score == 335


def test_get_all_solutions() -> None:
    filename = Path(__file__).parent / "data" / "stats.json"
    solutions = get_all_solutions(filename)
    assert len(solutions) == 4
