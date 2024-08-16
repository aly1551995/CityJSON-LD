import json
from typing import List, Dict, Any, Optional, Union
from Metadata.geographicalExtent import GeographicalExtent
from Cityobjects.Geometry.geometry import Geometry


class SecondLevelCityObject:
    type_values = ["BridgeConstructiveElement",
                   "BridgeFurniture",
                   "BridgePart",
                   "BridgeRoom",
                   "BridgeInstallation",
                   "BuildingConstructiveElement",
                   "BuildingFurniture",
                   "BuildingInstallation",
                   "BuildingPart",
                   "BuildingRoom",
                   "BuildingStorey",
                   "BuildingUnit",
                   "TunnelConstructiveElement",
                   "TunnelFurniture",
                   "TunnelHollowSpace",
                   "TunnelInstallation",
                   "TunnelPart"]

    def __init__(self, alias: str, id: str, type: str, parent: str, geometry: Optional[List[Geometry]], geographical_extent: Optional[GeographicalExtent] = None, attributes: Optional[Union[Dict[str, Any], str]] = None, children: Optional[List[str]] = None):
        """
        Initialize the SecondLevelCityObject with the given parameters.

        :param alias: Alias for the city object.
        :param id: Unique identifier for the city object.
        :param type: Type of the city object. Must be one of the predefined type_values.
        :param parent: Parent identifier for the city object.
        :param geometry: Geometry object representing the city's geometry.
        :param geographical_extent: GeographicalExtent object or None.
        :param attributes: Dictionary of attributes or None.
        :param children: List of children identifiers or None.
        """
        self.alias = alias
        self.id = id
        if type in self.type_values:
            self.type = type
        else:
            raise ValueError(
                f"type value must be one of {', '.join(self.type_values)}")
        self.parent = parent[0]
        self.geographical_extent = GeographicalExtent.to_geographical_extent(
            geographical_extent)
        self.attributes = json.dumps(attributes) if attributes else None
        self.children = children
        self.geometry = [geom.to_json()
                         for geom in geometry] if geometry else None

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the SecondLevelCityObject to a JSON-LD representation.

        :return: JSON-LD representation of the SecondLevelCityObject.
        """
        geometry = self.geometry if self.geometry else None
        geographical_extent_dict = json.loads(
            self.geographical_extent.to_json()) if self.geographical_extent else None
        attributes_dict = json.loads(
            self.attributes) if self.attributes else None
        children_list = [{"@id": f'{self.alias}:{child}'}
                         for child in self.children] if self.children else None

        data = {
            "@id": f'{self.alias}:{self.id}',
            "@type": "cj:SecondLevelCityObject",
            "cj:type": self.type,
            "cj:hasParent": {
                "@id": f'{self.alias}:{self.parent}'
            },
            "cj:hasGeographicalExtent": geographical_extent_dict,
            "cj:hasAttribute": {
                "@type": "@json",
                "@value": attributes_dict
            },
            "cj:hasGeometry": geometry
        }

        # Add "cj:hasChildren" only if there are children
        if children_list:
            data["cj:hasChildren"] = children_list

        # Filter out None values
        filtered_data = {key: value for key,
                         value in data.items() if value is not None}
        return filtered_data
