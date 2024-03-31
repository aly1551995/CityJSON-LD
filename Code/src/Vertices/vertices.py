from Vertices.vertex import Vertex


class Vertices:

    def __init__(self, vertices: list):
        self.vertices = self.to_vertices(vertices)

    def to_vertices(self, vertices):
        vertices_list = []
        if isinstance(vertices, list):
            for vertex in vertices:
                if isinstance(vertex, list) and len(vertex) == 3 and all(isinstance(coordinate, int) for coordinate in vertex):
                    vertices_list.append(
                        Vertex(vertex[0], vertex[1], vertex[2]))
                else:
                    print("Vertex should be a list of 3 integers")
            return vertices_list
        else:
            print("Vertices should be a list of of lists of 3 integers")

    def to_json(self):
        data = {
            "@type": "cj:Vertices",
            "@list": [vertex.to_json() for vertex in self.vertices]
        }
        return data
