import json
from typing import Dict, Any

class Scale:
    def __init__(self, x: float, y: float, z: float):
        """
        Initialize the Scale object with x, y, and z scale factors.

        :param x: Scale factor in the x direction.
        :param y: Scale factor in the y direction.
        :param z: Scale factor in the z direction.
        """
        self.x = x
        self.y = y
        self.z = z

    def to_json(self) -> str:
        """
        Convert the Scale object to a JSON-LD representation.

        :return: JSON-LD representation of the Scale object.
        """
        data = {
            "@type": "cj:Scale",
            "cj:scaleX": {
                "@value": float(self.x),
                "@type": "xsd:float"
            },
            "cj:scaleY": {
                "@value": float(self.y),
                "@type": "xsd:float"
            },
            "cj:scaleZ": {
                "@value": float(self.z),
                "@type": "xsd:float"
            }
        }
        return json.dumps(data, ensure_ascii=False)

