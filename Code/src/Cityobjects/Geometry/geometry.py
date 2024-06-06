from typing import Any, Dict, List, Tuple
from shapely.geometry import Polygon, MultiPoint, MultiLineString, MultiPolygon
from Cityobjects.Geometry.multiPoint import MultiPoint as CjMultiPoint
from Cityobjects.Geometry.multiLineString import MultiLineString as CjMultiLineString
from Cityobjects.Geometry.multiCompositeSurface import MultiCompositeSurface as CjMultiCompositeSurface
from Cityobjects.Geometry.solid import Solid as CjSolid
from Cityobjects.Geometry.multiCompositeSolid import MultiCompositeSolid as CjMultiCompositeSolid


class Geometry:
    """
    A class to represent a cityJSON geometric object with various types such as MultiPoint, MultiLineString, MultiSurface,
      CompositeSurface, Solid, MultiSolid, CompositeSolid.

    Attributes:
        type (str): The type of the geometric object.
        lod (str): The level of detail of the geometric object.
        boundaries (str): The boundaries of the geometric object in CityJSON format.
    """

    def __init__(self, type: str, lod: str, boundaries: List, vertices: List[Tuple[float, float, float]], scale: List[float], translate: List[float]):
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
        return (vertex[0] * scale[0] + translate[0], vertex[1] * scale[1] + translate[1], vertex[2] * scale[2] + translate[2])

    def point_to_wkt(self, points, vertices, scale, translate):
        """
        Convert (Multi)points to WKT format.

        :param points: List of points.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: (Multi)Points in 2D WKT format and (Multi)Points in 3D coordinates in JSON-LD format.
        """
        points_as_vertices_3d = [self.get_real_vertex(
            point, vertices, scale, translate) for point in points]
        # Convert to 2D by ignoring the Z-coordinate
        points_as_vertices_2d = [(pt[0], pt[1])
                                 for pt in points_as_vertices_3d]
        multi_point = MultiPoint(points_as_vertices_2d)
        return multi_point.wkt, points_as_vertices_3d

    def linestring_to_wkt(self, lines, vertices, scale, translate):
        """
        Convert (Multi)Linestrings to WKT format.

        :param lines: List of Lines.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: (Multi)Linestrings in WKT format and (Multi)LineStrings in 3D coordinates in JSON-LD format.
        """
        lines_as_vertices_3d = [[self.get_real_vertex(
            point, vertices, scale, translate) for point in line] for line in lines]
        # Convert to 2D by ignoring the Z-coordinate
        lines_as_vertices_2d = [[(pt[0], pt[1]) for pt in line]
                                for line in lines_as_vertices_3d]
        multi_line = MultiLineString(lines_as_vertices_2d)
        return multi_line.wkt, lines_as_vertices_3d

    def multi_surface_to_wkt(self, surfaces: List[List[List[int]]], vertices: List[Tuple[float, float, float]], scale: List[float], translate: List[float]) -> Tuple[str, List[List[List[Tuple[float, float, float]]]]]:
        """
        Convert multi-surfaces to WKT format.

        :param surfaces: List of surfaces.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: MultiSurfaces in WKT format and MultiSurfaces in 3D coordinates in JSON-LD format.
        """
        surfaces_as_vertices_3d = []
        polygons = []

        for surface in surfaces:
            exterior_ring = [self.get_real_vertex(
                idx, vertices, scale, translate) for idx in surface[0]]
            interior_rings = [[self.get_real_vertex(
                idx, vertices, scale, translate) for idx in ring] for ring in surface[1:]]

            # Ensure the rings are closed
            if exterior_ring[0] != exterior_ring[-1]:
                exterior_ring.append(exterior_ring[0])
            for ring in interior_rings:
                if ring[0] != ring[-1]:
                    ring.append(ring[0])

            # Convert to 2D by ignoring the Z-coordinate
            exterior_ring_2d = [(pt[0], pt[1]) for pt in exterior_ring]
            interior_rings_2d = [[(pt[0], pt[1]) for pt in ring]
                                 for ring in interior_rings]

            polygon = Polygon(exterior_ring_2d, interior_rings_2d)
            polygons.append(polygon)
            surfaces_as_vertices_3d.append([exterior_ring] + interior_rings)

        multi_polygon = MultiPolygon(polygons)
        return multi_polygon.wkt, surfaces_as_vertices_3d

    def solid_to_wkt(self, solid: List[List[List[List[int]]]], vertices: List[Tuple[float, float, float]], scale: List[float], translate: List[float]) -> Tuple[str, List[List[List[Tuple[float, float, float]]]]]:
        """
        Convert an array of multisurfaces (3D solid) to 2D WKT format by projection.

        :param solid: Array of multisurfaces.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: Solids in WKT format and Solids in 3D coordinates in JSON-LD format.
        """
        all_polygons = []
        all_shells_3d = []

        for shell in solid:
            shell_3d = []
            for surface in shell:
                surface_3d = []
                for boundary in surface:
                    surface_3d.append([self.get_real_vertex(
                        idx, vertices, scale, translate) for idx in boundary])
                shell_3d.append(surface_3d)
            all_shells_3d.append(shell_3d)

            for surface in shell_3d:
                for boundary in surface:
                    if len(boundary) >= 3:
                        polygon = Polygon([(pt[0], pt[1]) for pt in boundary]).convex_hull
                        # polygon = Polygon([(pt[0], pt[1]) for pt in boundary])
                        # if polygon.is_valid and not polygon.is_empty:
                        if polygon.is_valid and not polygon.is_empty and isinstance(polygon, Polygon):
                            all_polygons.append(polygon)

        # multipolygon = MultiPolygon(all_polygons).convex_hull
        multipolygon = MultiPolygon(all_polygons)
        return multipolygon.wkt, all_shells_3d

    def multi_solid_to_wkt(self, multi_solid: List[List[List[List[List[int]]]]], vertices: List[Tuple[float, float, float]], scale: List[float], translate: List[float]) -> Tuple[str, List[List[List[List[Tuple[float, float, float]]]]]]:
        """
        Convert an array of multi-solids to 2D WKT format by projection.

        :param multi_solid: Array of multi-solids.
        :param vertices: List of vertices.
        :param scale: The scale factors.
        :param translate: The translation factors.
        :return: MultiSolids in WKT format and MultiSolids in 3D coordinates in JSON-LD format.
        """
        all_multipolygons = []
        all_solids_3d = []

        for solid in multi_solid:
            solid_3d = []
            for shell in solid:
                shell_3d = []
                for surface in shell:
                    surface_3d = []
                    for boundary in surface:
                        surface_3d.append([self.get_real_vertex(
                            idx, vertices, scale, translate) for idx in boundary])
                    shell_3d.append(surface_3d)
                solid_3d.append(shell_3d)
            all_solids_3d.append(solid_3d)

            polygons = []
            for shell in solid_3d:
                for surface in shell:
                    for boundary in surface:
                        if len(boundary) >= 3:
                            polygon = Polygon([(pt[0], pt[1])
                                              for pt in boundary])
                            if polygon.is_valid and not polygon.is_empty:
                                polygons.append(polygon)

            if polygons:
                multipolygon = MultiPolygon(polygons)
                all_multipolygons.append(multipolygon)

        geometry_collection = MultiPolygon(all_multipolygons)
        return geometry_collection.wkt, all_solids_3d

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
            multi_point_wkt, multi_point_3d = self.point_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = CjMultiPoint(multi_point_3d)
            return multi_point_wkt

        elif self.type == "MultiLineString":
            multi_linestring_wkt, multi_linestring_3d = self.linestring_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = CjMultiLineString(multi_linestring_3d)
            return multi_linestring_wkt

        elif self.type in ["MultiSurface", "CompositeSurface"]:
            multi_surface_composite_wkt, multi_surface_composite_3d = self.multi_surface_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = CjMultiCompositeSurface(
                multi_surface_composite_3d, self.type)
            return multi_surface_composite_wkt

        elif self.type == "Solid":
            solid_wkt, solid_3d = self.solid_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = CjSolid(solid_3d)
            return solid_wkt

        elif self.type in ["MultiSolid", "CompositeSolid"]:
            multi_composite_solid_wkt, multi_composite_solid_3d = self.multi_solid_to_wkt(
                boundaries, vertices, scale, translate)
            self.boundingBox = CjMultiCompositeSolid(multi_composite_solid_3d)
            return multi_composite_solid_wkt

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the CityJSON Geometry object to a JSON-LD representation.

        :return: JSON-LD representation of the Geometry object.
        """
        data = {
            "@type": "cj:Geometry",
            "cj:type": self.type,
            "cj:lod": self.lod,
            "geosparql:asWKT": {
                "@value": self.boundaries,
                "@type": "geosparql:wktLiteral"
            },
            "cj:hasBoundingBox": self.boundingBox.to_json()
        }

        return data
