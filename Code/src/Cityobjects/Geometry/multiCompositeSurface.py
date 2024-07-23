from typing import List, Tuple, Dict, Any


class MultiCompositeSurface:
    def __init__(self, surfaces: List[List[Tuple[float, float, float]]], surface_type: str):
        """
        Initialize the MultiSurface object with the list of surfaces and type.

        :param surfaces: List of surfaces, where each surface is a list of vertex coordinates (List of floats).
        :param surface_type: Type of the surface (e.g., MultiSurface, CompositeSurface).
        """
        self.surfaces = surfaces
        self.surface_type = surface_type

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the Surface object to a JSON-LD representation.

        :return: JSON-LD representation of the Surface object.
        """
        data = {
            "@type": f"cj:{self.surface_type}",
            "cj:hasSurface": []
        }

        for surface in self.surfaces:
            surface_data = {
                "@type": "cj:Surface",
                "cj:hasExteriorBoundary": {
                    "@type": "cj:ExteriorBoundary",
                    "cj:hasLineString": [
                        {
                            "@type": "cj:LineString",
                            "cj:hasPoint": [
                                {
                                    "@type": "cj:Point",
                                    "cj:boundaryX": {"@value": point[0], "@type": "xsd:float"},
                                    "cj:boundaryY": {"@value": point[1], "@type": "xsd:float"},
                                    "cj:boundaryZ": {"@value": point[2], "@type": "xsd:float"}
                                } for point in line
                            ]
                        } for line in surface
                    ]
                }
            }

        data["cj:hasSurface"].append(surface_data)

        return data
