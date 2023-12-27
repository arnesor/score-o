from pathlib import Path

from scoreo.solution import check_solution


def test_check_solution() -> None:
    filename = Path(__file__).parent / "data" / "stats.json"
    check_solution(filename)
