from pathlib import Path

from scoreo.course import Control
from scoreo.course import Course


def test_add_control() -> None:
    course1 = Course()
    course1.add_control(Control("141", "10", "20"))
    assert len(course1.controls) == 1
    assert next(iter(course1.controls.values())).code == "141"

    course2 = Course()
    course2.add_control(Control("M1", "10", "20"))
    assert len(course2.controls) == 1
    assert next(iter(course2.controls.values())).code == "1"

    course3 = Course()
    course3.add_control(Control("S1", "10", "20"))
    assert len(course3.controls) == 0


def test_read_ocad_course_file() -> None:
    control_file = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    course = Course()
    course.read_ocad_course_file(control_file)
    assert len(course.controls) == 26
    assert len(course.control_order) == 26
    assert next(iter(course.controls.values())).terrain_x != 0
    assert next(iter(course.controls.values())).terrain_y != 0
    assert next(iter(course.controls.values())).score == 0


def test_write_opsolver_file(default_course: Course) -> None:
    control_file = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    opsolver_file = default_course.write_opsolver_file(control_file, 5100)
    assert opsolver_file.is_file()


def test_stop_distance(default_course: Course) -> None:
    stop_distance = default_course.get_stop_distance()
    assert stop_distance == 271


def test_solution_score(default_course: Course) -> None:
    assert default_course.solution_score([1, 25]) == 5
    assert default_course.solution_score([1, 17]) == 10
    assert default_course.solution_score([1, 16, 17]) == 20


def test_solution_length(default_course: Course) -> None:
    assert default_course.solution_length([1, 25]) == 261
    assert default_course.solution_length([1, 25, 17]) == 519
