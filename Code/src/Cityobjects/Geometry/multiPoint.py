from typing import List, Tuple, Dict, Any


class MultiPoint:
    def __init__(self, points: List[Tuple[float, float, float]]):
        """
        Initialize the MultiPoint object with a list of points.

        :param points: List of points, where each point is a List of floats [x, y, z].
        """
        self.points = points

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the MultiPoint object to a JSON-LD representation.

        :return: JSON-LD representation of the MultiPoint object.
        """
        data = {
            "@type": "cj:MultiPoint",
            "cj:hasPoint": [
                {
                    "@type": "cj:Point",
                    "cj:boundaryX": {
                        "@value": point[0],
                        "@type": "xsd:float"
                    },
                    "cj:boundaryY": {
                        "@value": point[1],
                        "@type": "xsd:float"
                    },
                    "cj:boundaryZ": {
                        "@value": point[2],
                        "@type": "xsd:float"
                    }
                } for point in self.points
            ]
        }
        return data
