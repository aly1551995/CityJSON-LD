import json
from typing import List, Dict, Any, Optional, Union
from Cityobjects.Geometry.geometry import Geometry
from Metadata.geographicalExtent import GeographicalExtent


class FirstLevelCityObject:
    type_values = ["Bridge",
                   "Building",
                   "CityFurniture",
                   "CityObjectGroup",
                   "GenericCityObject",
                   "LandUse",
                   "OtherConstruction",
                   "PlantCover",
                   "SolitaryVegetationObject",
                   "TINRelief",
                   "TransportationSquare",
                   "Railway",
                   "Road",
                   "Tunnel",
                   "WaterBody",
                   "Waterway"]

    def __init__(self, alias: str, id: str, type: str, geometry: Geometry, geographical_extent: Optional[GeographicalExtent] = None, attributes: Optional[Union[Dict[str, Any], str]] = None, children: Optional[List[str]] = None):
        """
        Initialize the FirstLevelCityObject with the given parameters.

        :param alias: Alias for the city object.
        :param id: Unique identifier for the city object.
        :param type: Type of the city object. Must be one of the predefined type_values.
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
            raise ValueError(f"type value must be one of {', '.join(self.type_values)}")
        self.geographical_extent = GeographicalExtent.to_geographical_extent(geographical_extent)
        self.attributes = attributes
        self.children = children
        self.geometry = geometry

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the FirstLevelCityObject to a JSON-LD representation.

        :return: JSON-LD representation of the FirstLevelCityObject.
        """
        geographical_extent_dict = json.loads(self.geographical_extent.to_json()) if self.geographical_extent else None

        # Check if self.attributes is None
        if not self.attributes:
            # If self.attributes is None or an empty string, set attributes_dict to None
            attributes_dict = None
        else:
            attributes_dict = self.attributes

        children_list = [{"@id": f'{self.alias}:{child}'}
                         for child in self.children] if self.children else None
                         
        data = {
            "@id": f'{self.alias}:{self.id}',
            "@type": "cj:FirstLevelCityObject",
            "cj:type": self.type,
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
