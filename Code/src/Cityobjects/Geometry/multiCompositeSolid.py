from typing import List, Tuple, Dict, Any


class MultiCompositeSolid:
    def __init__(self, solids: List[List[List[List[List[Tuple[float, float, float]]]]]], type: str):
        """
        Initialize the MultiSolid object with the list of Solids.

        :param solids: List of solids, where each solid is a list of shells,
                       each shell is a list of multisurfaces,
                       each multisurface is a list of boundaries,
                       and each boundary is a list of vertex coordinates (List of floats).
        :param type: The type of the multi-solid object, either 'MultiSolid' or 'CompositeSolid'.
        """
        self.solids = solids
        self.type = type

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the MultiSolid object to a JSON-LD representation.

        :return: JSON-LD representation of the MultiSolid object.
        """
        solid_data = {
            "@type": f"cj:{self.type}",
            "cj:hasSolid": []
        }

        for solid in self.solids:
            solid_entry = {
                "@type": "cj:Solid",
                "cj:hasExteriorShell": None,
                "cj:hasInteriorShell": []
            }
            for shell_index, shell in enumerate(solid):
                shell_type = "cj:ExteriorShell" if shell_index == 0 else "cj:InteriorShell"
                shell_data = {
                    "@type": shell_type,
                    "cj:hasSurface": []
                }
                for multisurface in shell:
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
                                } for line in multisurface
                            ]
                        }
                    }

                    # Handle interior boundaries if they exist
                    interior_boundary_lines = multisurface[1:]
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

                    shell_data["cj:hasSurface"].append(surface_data)

                if shell_index == 0:
                    solid_entry["cj:hasExteriorShell"] = shell_data
                else:
                    solid_entry["cj:hasInteriorShell"].append(shell_data)

            # Remove cj:hasInteriorShell if it's empty
            if not solid_entry["cj:hasInteriorShell"]:
                del solid_entry["cj:hasInteriorShell"]

            solid_data["cj:hasSolid"].append(solid_entry)

        return solid_data
