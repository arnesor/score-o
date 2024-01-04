from pathlib import Path

import pytest

from scoreo.course import Course
from scoreo.solution import Solution
from scoreo.solution import get_all_solutions


@pytest.fixture()
def default_course() -> Course:
    control_file = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    score_file = Path(__file__).parent / "data" / "race_230907.sco"
    course = Course()
    course.read_ocad_course_file(control_file)
    course.read_score_file(score_file)
    return course


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
def tsp_controls() -> list[int]:
    return [
        1,
        25,
        23,
        24,
        14,
        5,
        2,
        3,
        4,
        11,
        10,
        15,
        9,
        8,
        6,
        12,
        13,
        7,
        26,
        22,
        21,
        20,
        19,
        18,
        16,
        17,
    ]


@pytest.fixture()
def all_solutions() -> list[Solution]:
    filename = Path(__file__).parent / "data" / "stats-all.json"
    return get_all_solutions(filename)
