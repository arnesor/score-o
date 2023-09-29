"""Classes and functions for courses and controls."""


class Control:
    """A Class representing an orienteering control with position, code and points."""

    def __init__(self, code: str, x: str, y: str) -> None:
        self.code = code
        self.map_x = x
        self.map_y = y
        self.points = 0
        self.terrain_x = 0
        self.terrain_y = 0

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
        pass
