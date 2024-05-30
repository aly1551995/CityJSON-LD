import argparse
import json
import os
import validators
from urllib.parse import urlparse
from cjio import cityjson
from cjvalpy import cjvalpy
import pyshacl
from jsonpath_ng import parse
from Cityobjects.firstLevelCityObject import FirstLevelCityObject
from Cityobjects.SecondLevelCityObject import SecondLevelCityObject
from Cityobjects.Geometry.geometry import Geometry
from Vertices.vertices import Vertices
from Metadata.metadata import Metadata
from Transform.transform import Transform
from cityJson import CityJson


def extract_alias_from_base_url(url: str) -> str:
    """
    Extract the first two letters after "://" from the base URL.

    :param url: The base URL.
    :return: The extracted alias.
    """
    start_index = url.find("://")
    if start_index != -1:
        return url[start_index + 3:start_index + 5]
    else:
        raise ValueError("Invalid base URL")


def main(input_file_path: str, output_file_path: str, base_url: str, city_id: str, enable_shacl: bool):
    """
    Main function to process the CityJSON file and convert it to JSON-LD.

    :param input_file_path: Path to the input CityJSON file.
    :param output_file_path: Path to the output JSON file.
    :param base_url: Base URL for the CityJSON file.
    :param city_id: Identifier for the CityJSON file.
    :param enable_shacl: Flag to enable SHACL validation.
    """
    if not os.path.isabs(input_file_path):
        input_file_path = os.path.join(os.path.dirname(__file__), 'data', input_file_path)

    if not os.path.isabs(output_file_path):
        output_folder = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, output_file_path)

    cityjson_shacl_shapefile = os.path.join(os.path.dirname(__file__), 'SHACL', 'cityjsonShapes.ttl')

    with open(input_file_path) as file:
        file_content_json = json.load(file)
        file_content_str = json.dumps(file_content_json)
        val = cjvalpy.CJValidator([file_content_str])
        valid_city_json_file = val.validate()

        has_extension = "extensions" in file_content_json
        has_appearance = "appearance" in file_content_json
        has_geometry_templates = "geometry_templates" in file_content_json

        if valid_city_json_file and not has_appearance and not has_extension and not has_geometry_templates:
            cityjson_data = cityjson.load(input_file_path)
            has_metadata = cityjson_data.has_metadata()

            metadata_obj = None
            if has_metadata:
                metadata_values = cityjson_data.get_metadata()
                param_key_mapping = {
                    "geographical_extent": "geographicalExtent",
                    "identifier": "identifier",
                    "point_of_contact": "pointOfContact",
                    "reference_date": "referenceDate",
                    "reference_system": "referenceSystem",
                    "title": "title",
                }

                constructor_args = {
                    param: metadata_values[key]
                    for param, key in param_key_mapping.items()
                    if key in metadata_values and metadata_values[key] is not None
                }

                metadata_obj = Metadata(**constructor_args)

            transform_values = file_content_json["transform"]
            scale = transform_values["scale"]
            translate = transform_values["translate"]
            transform_obj = Transform(scale=scale, translate=translate)

            vertices = file_content_json["vertices"]
            vertices_obj = Vertices(vertices=vertices)
            version_value = file_content_json["version"]

            cityobjects = cityjson_data.get_cityobjects()
            cityobjects_keys = cityobjects.keys()
            cityobject_arry = []

            alias = extract_alias_from_base_url(base_url)

            for cityobject_key in cityobjects_keys:
                cityobject = cityobjects[cityobject_key]
                type = cityobject.type
                geographicalExtent = cityobject.geographicalExtent if hasattr(cityobject, 'geographicalExtent') else None
                attributes = cityobject.attributes if hasattr(cityobject, 'attributes') else None
                children = cityobject.children if hasattr(cityobject, 'children') else None
                geometry = file_content_json['CityObjects'][cityobject_key]['geometry'][0]
                cityobject_geometry = Geometry(
                    geometry['type'], geometry['lod'], geometry['boundaries'], vertices, scale, translate)

                if cityobject.type in FirstLevelCityObject.type_values:
                    co = FirstLevelCityObject(
                        alias, cityobject_key, type, cityobject_geometry, geographicalExtent, attributes, children)
                else:
                    parents = cityobject.parents if hasattr(cityobject, 'parents') else None
                    if not parents:
                        raise AttributeError("cityobject does not have 'parents' attribute")
                    co = SecondLevelCityObject(
                        alias, cityobject_key, type, parents, cityobject_geometry, geographicalExtent, attributes, children)
                cityobject_arry.append(co)

            cityjson_obj = CityJson(
                base_url, alias, city_id, version_value, transform_obj, vertices_obj, cityobject_arry, metadata_obj)

            if enable_shacl:
                data_graph_str = json.dumps(cityjson_obj.to_json(), indent=4, ensure_ascii=False)
                validation_result = pyshacl.validate(
                    data_graph=data_graph_str,
                    shacl_graph=cityjson_shacl_shapefile,
                    ont_graph=None,
                    data_graph_format="json-ld",
                    depth=999
                )

                conforms, results_graph, results_text = validation_result

                if conforms:
                    with open(output_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(cityjson_obj.to_json(), json_file, indent=4, ensure_ascii=False)
                    print(f"JSON written to: {output_file_path}")
                else:
                    print("Data does not conform to SHACL shapes. Validation errors:")
                    print(results_text)
            else:
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(cityjson_obj.to_json(), json_file, indent=4, ensure_ascii=False)
                print(f"JSON written to: {output_file_path}")

        else:
            if has_extension:
                print("This current version does not support cityjson files with extensions")
            if has_appearance:
                print("This current version does not support cityjson files with appearance")
            if has_geometry_templates:
                print("This current version does not support cityjson files with geometry_templates")
            if not valid_city_json_file:
                print("The provided file is not a valid cityjson file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='cj2jld',
        description='Convert CityJSON file to JSON-LD.',
        epilog='This tool is a prototype developed for a master\'s thesis project of the same name. Thank you for using cj2jld!'
    )

    parser.add_argument(
        '-i', '--input-file', help='Input CityJSON file path relative or absolute. If relative, the file should be in the data folder inside the src folder. (required)', required=True)
    parser.add_argument(
        '-o', '--output-file', help='Output JSON file path relative or absolute. If relative, the file will be placed in the output folder inside the src folder. (required)', required=True)
    parser.add_argument(
        '-b', '--base-url', help='The base URL (required)', required=True)
    
    id_group = parser.add_mutually_exclusive_group(required=True)
    id_group.add_argument(
        '-id', help='Give the ID of the supplied CityJSON file input')
    id_group.add_argument(
        '-idp', '--id-path', help='Give a path to a JSON file that contains metadata object with identifier key in it representing the ID of the supplied CityJSON file input')

    parser.add_argument(
        '-epyshacl', '--enable-pyshacl',
        action='store_true',
        help='To enable pyshacl validation (Warning: could potentially take a significant amount of time with big files; not recommended by default, false)')

    args = parser.parse_args()

    if args.id:
        city_id = args.id
    elif args.id_path:
        with open(args.id_path, 'r') as f:
            supplied_identifier_data = json.load(f)
        expression = parse("$.metadata.identifier")
        matches = [match.value for match in expression.find(supplied_identifier_data)]
        if matches:
            city_id = matches[0]
            print("Identifier found:", city_id)
        else:
            parser.error("Identifier not found in the JSON file.")

    main(args.input_file, args.output_file, args.base_url, city_id, args.enable_pyshacl)
