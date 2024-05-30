from typing import List, Tuple, Dict, Any


class MultiLineString:
    def __init__(self, lines: List[List[Tuple[float, float, float]]]):
        """
        Initialize the MultiLineString object with a list of lines.

        :param lines: List of lines, where each line is a list representing points [x, y, z].
        """
        self.lines = lines

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the MultiLineString object to a JSON-LD representation.

        :return: JSON-LD representation of the MultiLineString object.
        """
        data = {
            "@type": "cj:MultiLineString",
            "cj:hasLineString": [
                {
                    "@type": "cj:LineString",
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
                        } for point in line
                    ]
                } for line in self.lines
            ]
        }
        return data
