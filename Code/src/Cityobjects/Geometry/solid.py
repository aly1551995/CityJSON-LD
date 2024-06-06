from typing import List, Tuple, Dict, Any


class Solid:
    def __init__(self, shells: List[List[List[List[Tuple[float, float, float]]]]]):
        """
        Initialize the Solid object with the list of shells.

        :param shells: List of shells, where each shell is a list of multisurfaces,
                       each multisurface is a list of boundaries, and each boundary 
                       is a list of vertex coordinates (List of floats).
        """
        self.shells = shells

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the Solid object to a JSON-LD representation.

        :return: JSON-LD representation of the Solid object.
        """
        solid_data = {
            "@type": "cj:Solid",
            "cj:hasExteriorShell": None,
            "cj:hasInteriorShell": []
        }

        for shell_index, shell in enumerate(self.shells):
            shell_type = "cj:ExteriorShell" if shell_index == 0 else "cj:InteriorShell"
            shell_data = {
                "@type": shell_type,
                "cj:hasSurface": []
            }
            for multisurface in shell:
                surface_data = {
                    "@type": "cj:Surface",
                    "cj:hasExteriorBoundary": {
                        "@type": f"{shell_type}",
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
                # In the given example, it appears there are no interior boundaries, so this part is skipped

                shell_data["cj:hasSurface"].append(surface_data)

            if shell_index == 0:
                solid_data["cj:hasExteriorShell"] = shell_data
            else:
                solid_data["cj:hasInteriorShell"].append(shell_data)

        # Remove cj:hasInteriorShell if it's empty
        if not solid_data["cj:hasInteriorShell"]:
            del solid_data["cj:hasInteriorShell"]

        return solid_data
