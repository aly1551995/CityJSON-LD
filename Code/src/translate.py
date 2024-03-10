import json


class Translate:

    def __init__(self, x: float, y: float, z: float):

        self.x = x
        self.y = y
        self.z = z


    def to_json(self):
        data = {
            "@type": "cj:Translate",
            "cj:translateX": {
                "@value": self.x,
                "@type": "xsd:decimal"
            },
            "cj:translateY": {
                "@value": self.y,
                "@type": "xsd:decimal"
            },
            "cj:translateZ": {
                "@value": self.z,
                "@type": "xsd:decimal"
            }
        }
        return json.dumps(data, ensure_ascii=False)
