from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from scoreo.opsolver import find_all_solutions
from scoreo.opsolver import find_initial_solution
from scoreo.opsolver import run_opsolver
from scoreo.solution import Solution
from scoreo.solution import get_all_solutions


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


@pytest.fixture()
def all_solutions() -> list[Solution]:
    filename = Path(__file__).parent / "data" / "stats-all.json"
    return get_all_solutions(filename)


@pytest.mark.docker
def test_run_opsolver_docker(problem_file: Path) -> None:
    solution = run_opsolver(problem_file)
    assert solution.number_of_controls == 25
    assert solution.score == 335
    assert solution.distance == 4875


def test_run_opsolver(problem_file: Path, mocker: MockerFixture) -> None:
    mock_docker_run = mocker.patch("scoreo.opsolver.docker.run")

    solution = run_opsolver(problem_file)
    mock_docker_run.assert_called_once_with(
        "arneso/opsolver:1",
        ["opt", "--op-exact", "1", f"{str(problem_file.name)}"],
        remove=True,
        volumes=[(str(problem_file.parent), "/tmp")],  # nosec B108
    )
    assert solution.number_of_controls == 25
    assert solution.score == 335
    assert solution.distance == 4875


@pytest.mark.docker
def test_find_initial_solution_docker(problem_file: Path) -> None:
    solution = find_initial_solution(problem_file)
    assert solution.number_of_controls == 26
    assert solution.score == 340


def test_find_initial_solution(problem_file: Path, mocker: MockerFixture) -> None:
    mock_docker_run = mocker.patch("scoreo.opsolver.docker.run")

    solution_list = [
        Solution(335, 25, 4875, [1, 17], 5016, 26),
        Solution(340, 26, 6772, [1, 17], 10032, 26),
        Solution(340, 26, 5126, [1, 17], 6762, 26),
        Solution(340, 26, 5112, [1, 17], 5116, 26),
        Solution(335, 25, 4875, [1, 17], 5102, 26),
    ]
    mock_get_solution = mocker.patch("scoreo.opsolver.get_last_solution")
    mock_get_solution.side_effect = solution_list

    solution = find_initial_solution(problem_file)
    assert solution.number_of_controls == 26
    assert solution.score == 340
    mock_docker_run.assert_called()


@pytest.mark.docker
def test_find_all_solutions_docker(problem_file: Path) -> None:
    solutions = find_all_solutions(problem_file, 5200, 4800)
    assert solutions[0].number_of_controls == 26


def test_find_all_solutions(
    problem_file: Path, all_solutions: list[Solution], mocker: MockerFixture
) -> None:
    mock_docker_run = mocker.patch("scoreo.opsolver.docker.run")

    mock_get_solution = mocker.patch("scoreo.opsolver.get_last_solution")
    mock_get_solution.side_effect = all_solutions

    solutions = find_all_solutions(problem_file, 5200, 4800)
    mock_docker_run.assert_called()
    mock_get_solution.assert_called()
    assert solutions[-1].score == 330
    assert solutions[-1].distance == 4800
