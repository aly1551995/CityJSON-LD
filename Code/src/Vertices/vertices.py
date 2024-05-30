from typing import List, Dict, Any
from Vertices.vertex import Vertex

class Vertices:
    def __init__(self, vertices: List[List[int]]):
        """
        Initialize the Vertices object with a list of vertex coordinates.

        :param vertices: List of vertex coordinates.
        """
        self.vertices = self.to_vertices(vertices)

    def to_vertices(self, vertices: List[List[int]]) -> List[Vertex]:
        """
        Convert a list of vertex coordinates to a list of Vertex objects.

        :param vertices: List of vertex coordinates.
        :return: List of Vertex objects.
        """
        vertices_list = []
        if isinstance(vertices, list):
            for vertex in vertices:
                if isinstance(vertex, list) and len(vertex) == 3 and all(isinstance(coordinate, int) for coordinate in vertex):
                    vertices_list.append(Vertex(vertex[0], vertex[1], vertex[2]))
                else:
                    raise ValueError("Each vertex should be a list of 3 integers")
            return vertices_list
        else:
            raise TypeError("Vertices should be a list of lists of 3 integers")

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the Vertices object to a JSON-LD representation.

        :return: JSON-LD representation of the Vertices object.
        """
        data = {
            "@list": [vertex.to_json() for vertex in self.vertices]
        }
        return data
