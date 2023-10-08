"""A collection of useful functions.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""

from pathlib import Path

import defusedxml.ElementTree

from .course import Control
from .course import Course


def read_course_file(filename: Path) -> Course:
    """Reads an OCAD file and prints information about controls."""
    print(f"Parsing file {filename}")
    root = defusedxml.ElementTree.parse(filename).getroot()
    # root = tree.getroot()
    print(len(root))

    course = Course()
    tag_name = "{http://www.orienteering.org/datastandard/3.0}Control"
    for xml_control in root.iter(tag_name):
        id_ = ""
        for sub in list(xml_control):
            if sub.tag[-2:] == "Id":
                id_ = sub.text
            if sub.tag[-11:] == "MapPosition":
                x_pos = sub.attrib.get("x")
                y_pos = sub.attrib.get("y")
                # print(f"{id_}: {sub.attrib}")
                control = Control(id_, x_pos, y_pos)
                course.add_control(control)
                print(f"{id_}: {x_pos=} {y_pos=}")

    return course
