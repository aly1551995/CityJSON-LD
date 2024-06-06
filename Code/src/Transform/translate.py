import json
from typing import Dict, Any


class Translate:
    def __init__(self, x: float, y: float, z: float):
        """
        Initialize the Translate object with x, y, and z translation values.

        :param x: Translation value in the x direction.
        :param y: Translation value in the y direction.
        :param z: Translation value in the z direction.
        """
        self.x = x
        self.y = y
        self.z = z

    def to_json(self) -> str:
        """
        Convert the Translate object to a JSON-LD representation.

        :return: JSON-LD representation of the Translate object.
        """
        data = {
            "@type": "cj:Translate",
            "cj:translateX": {
                "@value": float(self.x),
                "@type": "xsd:float"
            },
            "cj:translateY": {
                "@value": float(self.y),
                "@type": "xsd:float"
            },
            "cj:translateZ": {
                "@value": float(self.z),
                "@type": "xsd:float"
            }
        }
        return json.dumps(data, ensure_ascii=False)
