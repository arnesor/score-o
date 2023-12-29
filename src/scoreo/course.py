"""Classes and functions for courses and controls."""
import csv
import math
from pathlib import Path

import defusedxml.ElementTree

# import matplotlib.pyplot as plt
import networkx as nx
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

    def estimate_max_distance(self) -> int:
        """Estimate the initial max distance for visiting all controls.

        Algorithm: Circumference of the bounding rectangle.

        Returns:
            The max distance in meters.
        """
        x_values = [control.terrain_x for control in self.controls.values()]
        y_values = [control.terrain_y for control in self.controls.values()]
        return 2 * (max(x_values) - min(x_values)) + 2 * (max(y_values) - min(y_values))

    def write_opsolver_file(self, source_file: Path, distance_limit: int) -> Path:
        """Write a problem file in oplib format for opsolver.

        The file format is described on
        https://github.com/bcamath-ds/OPLib/tree/master/instances

        Args:
            source_file: IOF xml file with control coordinates.
            distance_limit: The distance limit for the problem, in meters.

        Returns:
            The filename and path of the generated opsolver file.
        """
        basename = source_file.stem.split(".")[0]
        dir = source_file.parent / basename
        if not dir.is_dir():
            dir.mkdir()

        filename = dir / f"{basename}.oplib"
        with open(filename, "w") as file:
            file.write(f"NAME : {basename}\n")
            file.write("COMMENT : Orienteering problem generated from IOF xml file\n")
            file.write("TYPE : OP\n")
            file.write(f"DIMENSION : {len(self.controls)}\n")
            file.write(f"COST_LIMIT : {str(distance_limit)}\n")
            file.write("EDGE_WEIGHT_TYPE : EUC_2D\n")

            file.write("NODE_COORD_SECTION\n")
            for key, value in self.control_order.items():
                file.write(
                    f"{key} "
                    f"{self.controls.get(value).terrain_x} "  # type: ignore[union-attr]
                    f"{self.controls.get(value).terrain_y}\n"  # type: ignore[union-attr]
                )

            file.write("NODE_SCORE_SECTION\n")
            for key, value in self.control_order.items():
                file.write(f"{key} {self.controls.get(value).score}\n")  # type: ignore[union-attr]

            file.write("DEPOT_SECTION\n")
            file.write("1\n")
            file.write("-1\n")
            file.write("EOF\n")
        return filename

    def write_score_template(self, filename: Path) -> None:
        """Write a template file for setting scores on each control."""
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

    def display_controls(self, solution: list[int]) -> None:
        """Display the controls in a course based on their 'map_x' and 'map_y' attributes."""
        # Create a graph
        g = nx.Graph()

        # Add nodes (controls) to the graph
        for control in self.controls.values():
            g.add_node(
                self.control_order.inverse[control.code],
                pos=(control.map_x, control.map_y),
            )

        # Draw the graph
        pos = nx.get_node_attributes(g, "pos")
        nx.draw(g, pos, node_color="white", edgecolors="red", node_size=500)
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos, edgelist=g.edges(), edge_color="blue")

        # Add edges based on the solution
        if len(solution) > 1:
            for i in range(len(solution)):
                next_node = solution[i + 1] if i + 1 < len(solution) else solution[0]
                g.add_edge(str(solution[i]), str(next_node))
            nx.draw_networkx_edges(g, pos, edgelist=g.edges(), edge_color="blue")

        # plt.show()

    def get_stop_distance(self) -> int:
        """Get the distance to the control nearest the finish and back again.

        Returns:
            Distance running to the nearest control and back to finish.
        """
        pos = []
        for _, value in self.control_order.items():
            pos.append(
                (self.controls.get(value).terrain_x, self.controls.get(value).terrain_y)  # type: ignore[union-attr]
            )

        if len(pos) < 2:
            return 0  # No other coordinate to compare with

        first_coordinate = pos[0]
        min_distance = math.inf
        for coord in pos[1:]:
            distance = math.sqrt(
                (coord[0] - first_coordinate[0]) ** 2
                + (coord[1] - first_coordinate[1]) ** 2
            )
            if distance < min_distance:
                min_distance = distance

        margin = 10
        return math.ceil(min_distance * 2 + margin)
