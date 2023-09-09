from pathlib import Path

from scoreo.functions import read_course_file


def test_read_course_file() -> None:
    filename = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    read_course_file(filename)
    assert True
