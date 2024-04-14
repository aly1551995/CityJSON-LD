import json
from Metadata.geographicalExtent import GeographicalExtent
from Cityobjects.firstLevelCityObject import FirstLevelCityObject
from Cityobjects.geometry import Geometry


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

    def __init__(self, id: str, type: str, parent: str, geometry: Geometry, geographical_extent=None, attributes=None, children=None):
        self.id = id
        if type in self.type_values:
            self.type = type
        else:
            raise ValueError(
                f"type value must be one of {', '.join(self.type_values)}")
        self.parent = parent
        self.geographical_extent = GeographicalExtent.to_geographical_extent(
            geographical_extent)
        self.attributes = json.dumps(attributes)
        self.children = children
        self.geometry = geometry

    def to_json(self):
        geographical_extent_dict = json.loads(
            self.geographical_extent.to_json()) if self.geographical_extent else None
        attributes_dict = json.loads(
            self.attributes) if self.attributes else None
        children_list = [{"@id": f'ex:{child}'} for child in self.children]
        data = {
            "@id": f'ex:{self.id}',
            "@type": "cj:SecondLevelCityObject",
            "cj:type": self.type,
            "cj:hasParent": {
                "@id": f'ex:{self.parent[0]}'
            },
            "cj:hasGeographicalExtent": geographical_extent_dict,
            "cj:hasAttribute": attributes_dict,
            "cj:hasGeometry": self.geometry.to_json()
        }
       # Add "cj:hasChildren" only if there are children
        if children_list:
            data["cj:hasChildren"] = children_list

        # Filter out None values
        filtered_data = {key: value for key,
                         value in data.items() if value is not None}

        return filtered_data
