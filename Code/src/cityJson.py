from urllib.parse import urlparse
from typing import List, Dict, Any, Optional
from Transform.transform import Transform
from Vertices.vertices import Vertices
from Metadata.metadata import Metadata

class CityJSON:
    def __init__(self, base_url: str, alias: str, id: str, version: str, transform: Transform, vertices: Vertices, cityobjects: List[Any], metadata: Optional[Metadata] = None):
        """
        Initialize the CityJson object with the given parameters.

        :param base_url: Base URL for the CityJSON.
        :param alias: Alias for the CityJSON.
        :param id: Unique identifier for the CityJSON.
        :param version: Version of the CityJSON.
        :param transform: Transform object for the CityJSON.
        :param vertices: Vertices object for the CityJSON.
        :param cityobjects: List of city objects.
        :param metadata: Metadata object for the CityJSON, optional.
        """
        self.base_url = base_url
        self.alias = alias
        self.id = id
        if not self.is_url(self.id):
            self.id = f"{base_url.rstrip('/')}/{id}"  # Remove trailing '/'
        self.type = "CityJSON"
        self.version = version
        self.transform = transform
        self.vertices = vertices
        self.cityobjects = cityobjects
        self.metadata = metadata

    @staticmethod
    def is_url(url: str) -> bool:
        """
        Check if the given string is a valid URL.

        :param url: String to check.
        :return: True if the string is a valid URL, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the CityJson object to a JSON-LD representation.

        :return: JSON-LD representation of the CityJson object.
        """
        data = {
            "@context": {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "cj": "https://www.cityjson.org/ont/cityjson.ttl#",
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "geosparql": "http://www.opengis.net/ont/geosparql#",
                self.alias: self.base_url
            },
            "@id": self.id,
            "@type": "cj:CityJSON",
            "cj:type": self.type,
            "cj:version": self.version,
            "cj:hasVertices": self.vertices.to_json(),
            "cj:hasCityObjects": [cityobj.to_json() for cityobj in self.cityobjects],
            "cj:hasTransform": self.transform.to_json(),
            "cj:hasMetadata": self.metadata.to_json() if self.metadata else None
        }

        # Filter out None values
        filtered_data = {key: value for key, value in data.items() if value is not None}

        return filtered_data

