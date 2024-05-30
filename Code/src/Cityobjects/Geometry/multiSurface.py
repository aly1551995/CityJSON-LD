from typing import List, Tuple, Dict, Any


class MultiSurface:
    def __init__(self, surfaces: List[List[List[Tuple[float, float, float]]]], type: str):
        """
        Initialize the MultiSurface object with the list of surfaces and type.

        :param surfaces: List of surfaces, where each surface is a list of boundaries,
                         and each boundary is a list of vertex coordinates (List of floats).
        :param type: Type of the surface (e.g., MultiSurface, CompositeSurface).
        """
        self.surfaces = surfaces
        self.type = type

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the Surface object to a JSON-LD representation.

        :return: JSON-LD representation of the Surface object.
        """
        data = {
            "@type": f"cj:{self.type}",
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
                        } for line in surface[0]
                    ]
                }
            }

            # Handle interior boundaries if they exist
            interior_boundary_lines = surface[1:]
            if interior_boundary_lines:
                interior_boundaries = []
                for line in interior_boundary_lines:
                    interior_boundaries.append({
                        "@type": "cj:InteriorBoundary",
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
                            }
                        ]
                    })
                surface_data["cj:hasInteriorBoundary"] = interior_boundaries

            data["cj:hasSurface"].append(surface_data)

        return data
