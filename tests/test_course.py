from pathlib import Path

from scoreo.course import Course


def test_read_course_file() -> None:
    control_file = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    score_file = Path(__file__).parent / "data" / "race_230907.sco"
    course = Course()
    course.read_ocad_course_file(control_file)
    course.write_score_template()
    course.read_score_file(score_file)

    assert len(course.controls) == 26
    print(course)
