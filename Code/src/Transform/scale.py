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
                "@type": "xsd:float"
            },
            "cj:scaleY": {
                "@value": self.y,
                "@type": "xsd:float"
            },
            "cj:scaleZ": {
                "@value": self.z,
                "@type": "xsd:float"
            }
        }
        return json.dumps(data, ensure_ascii=False)
