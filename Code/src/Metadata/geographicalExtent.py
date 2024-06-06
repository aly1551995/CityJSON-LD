import json
from typing import List, Optional, Union


class GeographicalExtent:
    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float, min_z: float, max_z: float):
        """
        Initialize the GeographicalExtent object with minimum and maximum coordinates.

        :param min_x: Minimum X coordinate.
        :param max_x: Maximum X coordinate.
        :param min_y: Minimum Y coordinate.
        :param max_y: Maximum Y coordinate.
        :param min_z: Minimum Z coordinate.
        :param max_z: Maximum Z coordinate.
        """
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

    @staticmethod
    def to_geographical_extent(geographical_extent: Optional[List[float]]) -> Optional['GeographicalExtent']:
        """
        Convert a list of coordinates to a GeographicalExtent object.

        :param geographical_extent: List of 6 floats or None.
        :return: GeographicalExtent object or None.
        """
        if isinstance(geographical_extent, list):
            if len(geographical_extent) == 6:
                min_x, min_y, min_z, max_x, max_y, max_z = geographical_extent
                return GeographicalExtent(min_x, max_x, min_y, max_y, min_z, max_z)
            else:
                raise ValueError(
                    "Geographical Extent should be a list of 6 floats")
        elif geographical_extent is None:
            return None
        else:
            raise TypeError(
                "Geographical Extent should be either a list of 6 floats or None")

    def to_json(self) -> str:
        """
        Convert the GeographicalExtent object to a JSON-LD representation.

        :return: JSON-LD representation of the GeographicalExtent object.
        """
        data = {
            "@type": "cj:GeographicalExtent",
            "cj:minX": {
                "@value": float(self.min_x),
                "@type": "xsd:float"
            },
            "cj:maxX": {
                "@value": float(self.max_x),
                "@type": "xsd:float"
            },
            "cj:minY": {
                "@value": float(self.min_y),
                "@type": "xsd:float"
            },
            "cj:maxY": {
                "@value": float(self.max_y),
                "@type": "xsd:float"
            },
            "cj:minZ": {
                "@value": float(self.min_z),
                "@type": "xsd:float"
            },
            "cj:maxZ": {
                "@value": float(self.max_z),
                "@type": "xsd:float"
            },
        }
        return json.dumps(data, ensure_ascii=False)
