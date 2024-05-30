from Cityobjects.Geometry.multiPoint import MultiPoint
from Cityobjects.Geometry.multiLineString import MultiLineString
from Cityobjects.Geometry.multiSurface import MultiSurface


class Geometry:
    """
    A class to represent a cityJSON geometric object with various types such as MultiPoint, MultiLineString, MultiSurface, and CompositeSurface.

    Attributes:
        type (str): The type of the geometric object.
        lod (str): The level of detail of the geometric object.
        boundaries (str): The boundaries of the geometric object in CityJSON format.
    """

    def __init__(self, type: str, lod: str, boundaries: str, vertices, scale, translate):
        self.type = type
        self.lod = lod
        self.boundaries = self.to_wkt(boundaries, vertices, scale, translate)

    def get_real_vertex(self, index, vertices, scale, translate):
        """
        Replace vertex index with actual vertex coordinates and apply the transform function.

        :param index: The index of the vertex.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: Transformed vertex.
        """
        vertex = vertices[index]
        return vertex[0] * scale[0] + translate[0], vertex[1] * scale[1] + translate[1], vertex[2] * scale[2] + translate[2]

    def point_to_wkt(self, points, vertices, scale, translate):
        """
        Convert (Multi)points to WKT format.

        :param points: List of points.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: (Multi)Points in 2D WKT format and (Multi)Points in 3D coordinates.
        """
        points_as_vertices_2d = []
        points_as_vertices_3d = []
        for point in points:
            point_as_a_3D_vertex = self.get_real_vertex(
                point, vertices, scale, translate)
            point_as_a_2D_WKT_str = ' '.join(
                map(str, point_as_a_3D_vertex[:2]))
            points_as_vertices_2d.append(point_as_a_2D_WKT_str)
            points_as_vertices_3d.append(point_as_a_3D_vertex)
        points_list_to_string_2D = ', '.join(points_as_vertices_2d)
        return points_list_to_string_2D, points_as_vertices_3d

    def linestring_to_wkt(self, lines, vertices, scale, translate):
        """
        Convert (Multi)Linestrings to WKT format.

        :param lines: List of Lines.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: (Multi)Linestrings in WKT format and (Multi)LineStrings in 3D coordinates.
        """
        lines_as_vertices_2d = []
        lines_as_vertices_3d = []
        for lines in lines:
            points_list_to_string_2D, points_as_vertices_3d = self.point_to_wkt(
                lines, vertices, scale, translate)
            lines_as_vertices_2d.append(f'({points_list_to_string_2D})')
            lines_as_vertices_3d.append(points_as_vertices_3d)
        linstrings_list_to_string = ', '.join(lines_as_vertices_2d)
        return linstrings_list_to_string, lines_as_vertices_3d

    def multi_surface_to_wkt(self, surfaces, vertices, scale, translate):
        """
        Convert multi-surfaces to WKT format.

        :param surfaces: List of surfaces.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: MultiSurfaces in WKT format and MultiSurfaces in 3D coordinates.
        """
        surfaces_as_vertices_2d = []
        surfaces_as_vertices_3d = []
        for surface in surfaces:
            lines_as_vertices_3d = []
            exterior_ring = surface[0]
            exterior_ring.append(exterior_ring[0])
            interior_rings = surface[1:] if len(surface) > 1 else []
            wkt_surface = "(("
            points_list_to_string_2d, points_as_vertices_3d = self.point_to_wkt(
                exterior_ring, vertices, scale, translate)
            lines_as_vertices_3d.append(points_as_vertices_3d)
            wkt_surface += points_list_to_string_2d
            wkt_surface += ")"
            for ring in interior_rings:
                wkt_surface += ", ("
                ring.append(ring[0])
                points_list_to_string_2d, points_as_vertices_3d = self.point_to_wkt(
                    ring, vertices, scale, translate)
                lines_as_vertices_3d.append(points_as_vertices_3d)
                wkt_surface += points_list_to_string_2d
                wkt_surface += ")"
            wkt_surface += ")"
            surfaces_as_vertices_2d.append(wkt_surface)
            surfaces_as_vertices_3d.append([lines_as_vertices_3d])
        return surfaces_as_vertices_2d, surfaces_as_vertices_3d

    def to_wkt(self, boundaries, vertices, scale, translate):
        """
        Convert the cityJSON geometry boundaries to WKT format.

        :param boundaries: The boundaries of the geometric object.
        :param vertices: The vertices of the geometric object.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: Boundaries in WKT format.
        """
        if self.type == "MultiPoint":
            points_list_to_string_2d, points_list_3d = self.point_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = MultiPoint(points_list_3d)
            return "MULTIPOINT ({0})".format(points_list_to_string_2d)

        elif self.type == "MultiLineString":
            lines_list_to_string_2d, lines_list_3d = self.linestring_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = MultiLineString(lines_list_3d)
            return "MULTILINESTRING ({0})".format(lines_list_to_string_2d)

        elif self.type in ["MultiSurface", "CompositeSurface"]:
            multi_composite_surface_list_to_string_2d, multi_composite_surface_list_3d = self.multi_surface_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = MultiSurface(
                multi_composite_surface_list_3d, self.type)
            return "MULTIPOLYGON ({0})".format(multi_composite_surface_list_to_string_2d).replace("[", "").replace("]", "").replace("'", "")

    def to_json(self):
        """
        Convert the CityJSON Geometry object to a JSON-LD representation.

        :return: JSON-LD representation of the Geometry object.
        """
        data = {
            "@type": "cj:Geometry",
            "cj:type": self.type,
            "cj:lod": self.lod,
            "geo:asWKT": {
                "@value": self.boundaries,
                "@type": "geo:wktLiteral"
            },
            "cj:hasBoundingBox": self.boundingBox.to_json()
        }

        # return data
        return data
