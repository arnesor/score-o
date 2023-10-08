"""Classes and functions for courses and controls."""


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

    def __repr__(self) -> str:
        result = ""
        for _, control in self.controls.items():
            result += str(control) + "\n"
        return result

    def add_control(self, control: Control) -> None:
        """Add a control to the course."""
        key = control.code
        self.controls[key] = control
