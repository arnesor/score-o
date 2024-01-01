from pathlib import Path

import pytest

from scoreo.course import Course


@pytest.fixture()
def default_course() -> Course:
    control_file = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    score_file = Path(__file__).parent / "data" / "race_230907.sco"
    course = Course()
    course.read_ocad_course_file(control_file)
    course.read_score_file(score_file)
    return course


def test_read_course_file(default_course: Course) -> None:
    control_file = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    # course.write_score_template()
    default_course.write_opsolver_file(control_file, 5100)

    solution = [
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
    default_course.display_controls(solution)
    assert len(default_course.controls) == 26
    stop_distance = default_course.get_stop_distance()
    assert stop_distance == 271


def test_solution_score(default_course: Course) -> None:
    assert default_course.solution_score([1, 25]) == 5
    assert default_course.solution_score([1, 17]) == 10
    assert default_course.solution_score([1, 16, 17]) == 20


def test_solution_length(default_course: Course) -> None:
    assert default_course.solution_length([1, 25]) == 261
    assert default_course.solution_length([1, 25, 17]) == 519
