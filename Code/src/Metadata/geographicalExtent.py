import json


class GeographicalExtent:

    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float, min_z: float, max_z: float):

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

    @staticmethod
    def to_geographical_extent(geographical_extent):
        if isinstance(geographical_extent, list):
            if len(geographical_extent) == 6:
                min_x, min_y, min_z, max_x, max_y, max_z = geographical_extent
                return GeographicalExtent(min_x, min_y, min_z, max_x, max_y, max_z)
            else:
                print("Geographical Extent should be a list of 6 floats")
        elif not geographical_extent:
            return geographical_extent
        else:
            print("Geographical Extent should be either a GeographicalExtent object or a list of 6 floats or None")

    def to_json(self):
        data = {
            "@type": "cj:GeographicalExtent",
            "cj:minX": {
                "@value": self.min_x,
                "@type": "xsd:float"
            },
            "cj:maxX": {
                "@value": self.min_y,
                "@type": "xsd:float"
            },
            "cj:minY": {
                "@value": self.min_z,
                "@type": "xsd:float"
            },
            "cj:maxY": {
                "@value": self.max_x,
                "@type": "xsd:float"
            },
            "cj:minZ": {
                "@value": self.max_y,
                "@type": "xsd:float"
            },
            "cj:maxZ": {
                "@value": self.max_z,
                "@type": "xsd:float"
            }
        }
        return json.dumps(data, ensure_ascii=False)
