import json

class Geometry:

    def __init__(self, type: str, lod: str, boundaries: str, vertices, scale, translate):

        self.type = type
        self.lod = lod
        self.boundaries = self.to_wkt(boundaries, vertices, scale, translate)

    def to_wkt(self, boundaries, vertices, scale, translate):
        def apply_transform(vertex):
            return vertex[0] * scale[0] + translate[0], vertex[1] * scale[1] + translate[1]

        def replace_indices_with_vertices(index):
            return apply_transform(vertices[index])

        def point_to_wkt(points):
            points_as_vertices = []
            for point in points:
                point_as_vertex = replace_indices_with_vertices(point)
                point_as_str = '{0}'.format(
                    ' '.join(map(str, point_as_vertex)))
                points_as_vertices.append(point_as_str)
            points_list_to_string = ', '.join(points_as_vertices)
            return points_list_to_string
        
        def linestring_to_wkt(boundaries):
            lines_as_vertices = []
            for lines in boundaries:
                lines_as_vertices.append(f'({point_to_wkt(lines)})')
            linstrings_list_to_string = ', '.join(lines_as_vertices)
            return linstrings_list_to_string
        
        def multi_surface_to_wkt(surfaces):
            # print(surfaces)
            wkt_surfaces = []
            for surface in surfaces:
                # print(surface)
                exterior_ring = surface[0]
                # print(exterior_ring)
                interior_rings = surface[1:] if len(surface) > 1 else []
                # print(interior_rings)
                wkt_surface = "(("
                wkt_surface += point_to_wkt(exterior_ring)
                wkt_surface += ")"
                # print(wkt_surface)
                for ring in interior_rings:
                    wkt_surface += ", ("
                    wkt_surface += point_to_wkt(ring)
                    wkt_surface += ")"
                wkt_surface += ")"
                # print(wkt_surface)
                wkt_surfaces.append(wkt_surface)
                # print(wkt_surfaces)
            return "MULTIPOLYGON ({})".format(",".join(wkt_surfaces))

        if self.type == "MultiPoint":
            return "MULTIPOINT ({0})".format(point_to_wkt(boundaries))
        
        elif self.type == "MultiLineString":
            return "MULTILINESTRING ({0})".format(linestring_to_wkt(boundaries))
        
        elif self.type in ["MultiSurface", "CompositeSurface"]:
            return multi_surface_to_wkt(boundaries)

    def to_json(self):
        data = {
            "@type": "geo:Geometry",
            "cj:type": self.type,
            "cj:lod": self.lod,
            "geo:asWKT": {
                "@value": self.boundaries,
                "@type": "geo:wktLiteral"
            }
        }
        return data
