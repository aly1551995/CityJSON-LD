import argparse
import json
import os
import sys
from cjio import cityjson
from cjvalpy import cjvalpy
from Cityobjects.firstLevelCityObject import FirstLevelCityObject
from Cityobjects.SecondLevelCityObject import SecondLevelCityObject
from Vertices.vertices import Vertices
from Metadata.metadata import Metadata
from Transform.transform import Transform
from cityJson import CityJson


def main(input_file_path, output_file_path):
    # If the provided path is relative, open the file in the 'data' folder in the source directory
    if not os.path.isabs(input_file_path):
        input_file_path = os.path.join(os.path.dirname(__file__), 'data', input_file_path)

    # If the provided path is relative, save the file in the 'output' folder in the source directory
    if not os.path.isabs(output_file_path):
        output_folder = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, output_file_path)

    with open(input_file_path) as file:  # Open the provided cityjson file
        file_content_json = json.load(file)  # Read the file as a Python dict
        # Transform the Python dict to a JSON string
        file_content_str = json.dumps(file_content_json)
        # Get all first level keys in the Python dict
        file_content_keys = file_content_json.keys()
        # Create a CJValidator object using the provided CityJSON data as a list of strings
        val = cjvalpy.CJValidator([file_content_str])
        # Validate the CityJSON data using the CJValidator instance
        valid_city_json_file = val.validate()
        # Check if the file contains extensions
        has_extension = "extensions" in file_content_keys
        # Check if the file contains appearance
        has_appearance = "appearance" in file_content_keys
        # Check if the file contains geometry_templates
        has_geometry_templates = "geometry_templates" in file_content_keys

        # Check if the provided file is a valid cityjson file and doesn't have extensions, appearance, nor geometry templates
        if valid_city_json_file and not has_appearance and not has_extension and not has_geometry_templates:
            # Load the CityJSON data from the specified file path
            cityjson_data = cityjson.load(input_file_path)
            has_metadata = cityjson_data.has_metadata()  # Check if the file has metadata

            if has_metadata:
                # Extract metadata values from the loaded CityJSON data
                metadata_values = cityjson_data.get_metadata()
                # Define a mapping of the metadata object's parameter names to the keys in the metadata_values dictionary
                param_key_mapping = {
                    "geographical_extent": "geographicalExtent",
                    "identifier": "identifier",
                    "point_of_contact": "pointOfContact",
                    "reference_date": "referenceDate",
                    "reference_system": "referenceSystem",
                    "title": "title",
                }

                # Dynamically build constructor arguments if they exist and are not None
                constructor_args = {
                    param: metadata_values[key]
                    for param, key in param_key_mapping.items()
                    if key in metadata_values and metadata_values[key] is not None
                }

                # Create the Metadata object with the filtered arguments
                metadata_obj = Metadata(**constructor_args)

                # Extract transform values from the loaded CityJSON Python dict
                transform_values = file_content_json["transform"]
                # Extract scale values from the transform_values
                scale = transform_values["scale"]
                # Extract translate values from the transform_values
                translate = transform_values["translate"]
                # Create the Transform object
                transform_obj = Transform(scale=scale, translate=translate)

                # Extract vertices values from the loaded CityJSON Python dict
                vertices = file_content_json["vertices"]
                # Create the Vertices object
                vertices_obj = Vertices(vertices=vertices)
                # Extract version value from the loaded CityJSON Python dict
                version_value = file_content_json["version"]

                cityobjects = cityjson_data.get_cityobjects()
                cityobjects_keys = cityobjects.keys()
                cityobject_arry = []
                for cityobject_key in cityobjects_keys:
                    cityobject = cityobjects[cityobject_key]
                    type = cityobject.type
                    geographicalExtent = cityobject.geographicalExtent if hasattr(
                        cityobject, 'geographicalExtent') else None
                    attributes = cityobject.attributes if hasattr(
                        cityobject, 'attributes') else None
                    children = cityobject.children if hasattr(
                        cityobject, 'children') else None
                    if (cityobject.type in FirstLevelCityObject.type_values):
                        co = FirstLevelCityObject(
                            cityobject_key, type, geographicalExtent, attributes, children)
                    else:
                        if hasattr(cityobject, 'parents'):
                            parents = cityobject.parents
                        else:
                            raise AttributeError(
                                "cityobject does not have 'parents' attribute")
                        co = SecondLevelCityObject(
                            cityobject_key, type, parents, geographicalExtent, attributes, children)
                    cityobject_arry.append(co)
                cityjson_obj = CityJson(
                    version_value, transform_obj, vertices_obj, cityobject_arry, metadata_obj)

                # Write JSON to file
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(cityjson_obj.to_json(), json_file, indent=4, ensure_ascii=False)

                print(f"JSON written to: {output_file_path}")

        elif has_extension:
            print("This current version does not support cityjson files with extensions")
        elif has_appearance:
            print("This current version does not support cityjson files with appearance")
        elif has_geometry_templates:
            print(
                "This current version does not support cityjson files with geometry_templates")
        else:
            print("The provided file is not a valid cityjson file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CityJSON file to JSON-LD.')
    parser.add_argument('input_file', help='Input CityJSON file path relative or absolute if relative the file should be in data folder inside the src folder')
    parser.add_argument('output_file', help='Output JSON file path relative or absolute if relative the file will be placed in output folder inside the src folder')
    args = parser.parse_args()

    main(args.input_file, args.output_file)
