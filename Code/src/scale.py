import json


class Scale:

    def __init__(self, x: float, y: float, z: float):

        self.x = x
        self.y = y
        self.z = z


    def to_json(self):
        data = {
            "@type": "cj:Scale",
            "cj:scaleX": {
                "@value": self.x,
                "@type": "xsd:decimal"
            },
            "cj:scaleY": {
                "@value": self.y,
                "@type": "xsd:decimal"
            },
            "cj:scaleZ": {
                "@value": self.z,
                "@type": "xsd:decimal"
            }
        }
        return json.dumps(data, ensure_ascii=False)
