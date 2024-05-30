from typing import Any, Dict

class Vertex:
    def __init__(self, x: int, y: int, z: int):
        """
        Initialize the Vertex object with x, y, and z coordinates.

        :param x: X coordinate.
        :param y: Y coordinate.
        :param z: Z coordinate.
        """
        self.x = x
        self.y = y
        self.z = z

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the Vertex object to a JSON-LD representation.

        :return: JSON-LD representation of the Vertex object.
        """
        data = {
            "@type": "cj:Vertex",
            "cj:vertexX": self.x,
            "cj:vertexY": self.y,
            "cj:vertexZ": self.z
        }
        return data
