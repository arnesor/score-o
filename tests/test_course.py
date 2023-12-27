from pathlib import Path

from scoreo.course import Course


def test_read_course_file() -> None:
    control_file = Path(__file__).parent / "data" / "race_230907.Courses.xml"
    score_file = Path(__file__).parent / "data" / "race_230907.sco"
    course = Course()
    course.read_ocad_course_file(control_file)
    # course.write_score_template()
    course.read_score_file(score_file)
    course.write_opsolver_file(control_file, 5100)

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
    course.display_controls(solution)
    assert len(course.controls) == 26
    print(course)
