"""Test cases for the __main__ module."""
from pathlib import Path

import pytest
from click.testing import CliRunner

from scoreo import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    filename = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    result = runner.invoke(
        __main__.main,
        [str(filename), "--stop", "4800"],
    )
    assert result.exit_code == 0
