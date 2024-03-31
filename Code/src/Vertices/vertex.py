class Vertex:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def to_json(self):
        data = {
            "@type": "cj:Vertex",
            "cj:vertexX": self.x,
            "cj:vertexY": self.y,
            "cj:vertexZ": self.z
        }
        return data