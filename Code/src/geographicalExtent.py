import json


class GeographicalExtent:

    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float, min_z: float, max_z: float):

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z


    def to_json(self):
        data = {
            "@type": "cj:GeographicalExtent",
            "cj:minX": {
                "@value": self.min_x,
                "@type": "xsd:decimal"
            },
            "cj:maxX": {
                "@value": self.min_y,
                "@type": "xsd:decimal"
            },
            "cj:minY": {
                "@value": self.min_z,
                "@type": "xsd:decimal"
            },
            "cj:maxY": {
                "@value": self.max_x,
                "@type": "xsd:decimal"
            },
            "cj:minZ": {
                "@value": self.max_y,
                "@type": "xsd:decimal"
            },
            "cj:maxZ": {
                "@value": self.max_z,
                "@type": "xsd:decimal"
            }
        }
        return json.dumps(data, ensure_ascii=False)
