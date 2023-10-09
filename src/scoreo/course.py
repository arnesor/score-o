"""Classes and functions for courses and controls."""
from pathlib import Path

import defusedxml.ElementTree


class Control:
    """A Class representing an orienteering control with position, code and points."""

    multiplier = 10

    def __init__(self, code: str, x: str, y: str) -> None:
        self.code = code
        self.map_x = int(float(x) * Control.multiplier)
        self.map_y = int(float(y) * Control.multiplier)
        self.points = 0
        self.terrain_x = 0
        self.terrain_y = 0

    def __repr__(self) -> str:
        return (
            f"Control({self.code}, {self.map_x}, {self.map_y}, {self.terrain_x}, "
            f"{self.terrain_y}, {self.points})"
        )

    def set_terrain_position(
        self, scale: int, terrain_offset_x: int, terrain_offset_y: int
    ) -> None:
        """Set the geographic position of the map area, using offsets in meters.

        Args:
            scale: The denominator in the map scale. Example 1:10000 -> 10000.
            terrain_offset_x: Offset in north direction, measured in meters.
            terrain_offset_y: Offset in east direction, measured in meters.
        """
        pass


class Course:
    """A Class representing a collection of controls."""

    def __init__(self) -> None:
        self.controls: dict[str, Control] = {}
        self.map_scale = 5000

    def __repr__(self) -> str:
        result = ""
        for _, control in self.controls.items():
            result += str(control) + "\n"
        result += f"Map scale: {self.map_scale}"
        return result

    def add_control(self, control: Control) -> None:
        """Add a control to the course."""
        key = control.code
        self.controls[key] = control

    def read_ocad_course_file(self, filename: Path) -> None:
        """Reads an OCAD file and prints information about controls."""
        print(f"Parsing file {filename}")
        root = defusedxml.ElementTree.parse(filename).getroot()

        # Get map scale
        namespace = {"ns": "http://www.orienteering.org/datastandard/3.0"}
        scale_element = root.find(".//ns:Scale", namespace)
        if scale_element is not None:
            self.map_scale = int(scale_element.text)

        # For each control, get id and map position
        for xml_control in root.findall(".//ns:Control", namespace):
            id_element = xml_control.find("ns:Id", namespace)
            pos_element = xml_control.find("ns:MapPosition", namespace)
            if id_element is not None and pos_element is not None:
                id_ = id_element.text
                x_pos = pos_element.get("x")
                y_pos = pos_element.get("y")
                control = Control(id_, x_pos, y_pos)
                self.add_control(control)
