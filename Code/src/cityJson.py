import json
from Transform.transform import Transform
from Vertices.vertices import Vertices


class CityJson:

    def __init__(self, version: str, transform: Transform, vertices: Vertices, cityobjects, metadata=None):
        self.type = "CityJSON"
        self.version = version
        self.transform = transform
        self.vertices = vertices
        self.cityobjects = cityobjects
        self.metadata = metadata

    def to_json(self):
        data = {

            "@context": {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "cj": "https://www.cityjson.org/ont/cityjson.ttl#",
                "sh": "http://www.w3.org/ns/shacl#",
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "geo": "http://www.opengis.net/ont/geosparql#",
                "ex": "http://example.com/"
            },
            "@id": "http://example.com/Cityjson",
            "@type": "cj:Cityjson",
            "cj:type": self.type,
            "cj:version": self.version,
            "cj:hasVertices": self.vertices.to_json(),
            "cj:hasCityObjects": [cityobj.to_json() for cityobj in self.cityobjects],
            "cj:hasTransform": self.transform.to_json(),
            "cj:hasMetadata": self.metadata.to_json()
        }

        # Filter out None values
        filtered_data = {key: value for key,
                         value in data.items() if value is not None}
        return filtered_data