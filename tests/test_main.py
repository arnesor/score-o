"""Test cases for the __main__ module."""
from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from scoreo import __main__
from scoreo.solution import Solution


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.mark.docker
def test_main_succeeds_docker(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    filename = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    result = runner.invoke(
        __main__.main,
        [str(filename), "--stop", "4800"],
    )
    assert result.exit_code == 0


def test_main_succeeds(
    runner: CliRunner, all_solutions: list[Solution], mocker: MockerFixture
) -> None:
    mock_docker_run = mocker.patch("scoreo.opsolver.docker.run")

    mock_get_solution = mocker.patch("scoreo.opsolver.get_last_solution")
    mock_get_solution.side_effect = all_solutions

    filename = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    result = runner.invoke(
        __main__.main,
        [str(filename), "--stop", "4800"],
    )
    assert result.exit_code == 0
    mock_docker_run.assert_called()
    mock_get_solution.assert_called()
