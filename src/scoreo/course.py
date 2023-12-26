"""Classes and functions for courses and controls."""
import csv
from pathlib import Path

import defusedxml.ElementTree
from bidict import bidict


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
        self.score = 0

    def __repr__(self) -> str:
        return f"{self.code} {self.terrain_x} {self.terrain_y} {self.score}"
        #
        # return (
        #     f"Control({self.code}, {self.map_x}, {self.map_y}, {self.terrain_x}, "
        #     f"{self.terrain_y}, {self.points})"
        # )

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
        self.control_order: bidict[str, str] = bidict()
        self.map_scale = 5000

    def __repr__(self) -> str:
        result = ""
        for _, control in self.controls.items():
            result += str(control) + "\n"
        result += f"Map scale: {self.map_scale}\n"
        result += f"Control order: {self.control_order}\n"
        return result

    def add_control(self, control: Control) -> None:
        """Add a control to the course."""
        if control.code[0] in {"M", "F"}:
            control.code = "1"  # Code for finish
        if control.code.isdigit():
            self.controls[control.code] = control

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

        self.set_terrain_coordinates()

        # opsolver needs sorted sequential numbers for the controls.
        # Sort and make a mapping between sequential number and control code.
        self.controls = dict(sorted(self.controls.items()))
        for count, control_code in enumerate(self.controls, start=1):
            self.control_order[str(count)] = control_code

    def set_terrain_coordinates(self) -> None:
        """Set terrain coordinates in meters, using an offset to get positive numbers."""
        ll = self._get_lower_left()
        mm_to_m = 1000  # Number of millimeters in one meter
        scale_factor = int(self.map_scale / Control.multiplier / mm_to_m)
        for control in self.controls.values():
            control.terrain_x = (control.map_x - ll["min_x"]) * scale_factor
            control.terrain_y = (control.map_y - ll["min_y"]) * scale_factor

    def _get_lower_left(self) -> dict[str, int]:
        map_x_values = [control.map_x for control in self.controls.values()]
        map_y_values = [control.map_y for control in self.controls.values()]
        return {
            "min_x": min(map_x_values),
            "min_y": min(map_y_values),
        }

    def write_opsolver_file(self) -> None:
        """Write a problem file in oplib format for opsolver."""
        # Opsolver needs sequential numbers 1..number of controls.
        # Use bidict to store mapping between sequential numbers and control codes
        # for control_mapping in self.control_order:
        pass

    def write_score_template(self) -> None:
        """Write a template file for setting scores on each control."""
        filename = Path("score_template.sco")
        content = "\n".join(f"{key}, " for key in self.controls.keys())
        filename.write_text(content)
        print(f"Wrote file {filename}")

    def read_score_file(self, filename: Path) -> None:
        """Reads a score file with the score of each control.

        Format: control_id, score
        Only scores from controls matching the control keys from the imported OCAD-file
        will be imported.

        Args:
            filename: Name of the score file
        """
        print(f"Reading score file {filename}")

        with open(filename) as file:
            reader = csv.reader(file)
            for row in reader:
                control_id, score = row
                if control_id in self.controls:
                    self.controls[control_id].score = int(score)
