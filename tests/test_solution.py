from pathlib import Path

from scoreo.solution import get_solution


def test_get_solution() -> None:
    filename = Path(__file__).parent / "data" / "stats.json"
    solution = get_solution(filename)
    print(solution)
