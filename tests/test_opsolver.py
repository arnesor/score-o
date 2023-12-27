from pathlib import Path

from scoreo.opsolver import run_opsolver


def test_run_opsolver():
    problem = Path(__file__).parent / "data" / "race_230907-5016.oplib"
    run_opsolver(problem)


if __name__ == "__main__":
    test_run_opsolver()
