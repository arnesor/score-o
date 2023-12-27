from pathlib import Path

import pytest

from scoreo.opsolver import run_opsolver


@pytest.fixture()
def problem_file(tmp_path: Path) -> Path:
    """Copy the test problem file to a temporary directory."""
    source = Path(__file__).parent / "data" / "race_230907-5016.oplib"
    destination = tmp_path / source.name
    destination.write_bytes(source.read_bytes())
    return destination


def test_run_opsolver(problem_file: Path) -> None:
    run_opsolver(problem_file)
