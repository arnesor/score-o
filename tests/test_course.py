from pathlib import Path

from scoreo.course import Course


def test_read_course_file() -> None:
    filename = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    course = Course()
    course.read_ocad_course_file(filename)
    assert len(course.controls) == 27
