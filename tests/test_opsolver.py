from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from scoreo.opsolver import find_all_solutions
from scoreo.opsolver import find_initial_solution
from scoreo.opsolver import run_opsolver


@pytest.fixture()
def problem_file(tmp_path: Path) -> Path:
    """Copy the test problem file to a temporary directory."""
    source1 = Path(__file__).parent / "data" / "race_230907-5016.oplib"
    destination1 = tmp_path / source1.name
    destination1.write_bytes(source1.read_bytes())

    source2 = Path(__file__).parent / "data" / "stats.json"
    destination2 = tmp_path / source2.name
    destination2.write_bytes(source2.read_bytes())
    return destination1


def test_run_opsolver(problem_file: Path, mocker: MockerFixture) -> None:
    mock_docker_run = mocker.patch("scoreo.opsolver.docker.run")

    solution = run_opsolver(problem_file)

    # Assertions to ensure docker.run was called correctly
    mock_docker_run.assert_called_once_with(
        "arneso/opsolver:1",
        ["opt", "--op-exact", "1", f"{str(problem_file.name)}"],
        remove=True,
        volumes=[(str(problem_file.parent), "/tmp")],  # nosec B108
    )

    assert solution.number_of_controls == 25
    assert solution.score == 335
    assert solution.distance == 4875


@pytest.mark.skip(reason="Need to mock docker before running this test")
def test_find_initial_solution(problem_file: Path) -> None:
    solution = find_initial_solution(problem_file)
    assert solution.number_of_controls == 26
    assert solution.score == 340


@pytest.mark.skip(reason="Need to mock docker before running this test")
def test_find_all_solutions(problem_file: Path) -> None:
    solutions = find_all_solutions(problem_file, 5200, 4800)
    assert solutions[0].number_of_controls == 26
