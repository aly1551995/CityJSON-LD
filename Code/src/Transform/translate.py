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
                "@type": "xsd:float"
            },
            "cj:translateY": {
                "@value": self.y,
                "@type": "xsd:float"
            },
            "cj:translateZ": {
                "@value": self.z,
                "@type": "xsd:float"
            }
        }
        return json.dumps(data, ensure_ascii=False)
