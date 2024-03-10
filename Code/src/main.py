# main.py
import json
from cjio import cityjson
from cjvalpy import cjvalpy
from metadata import Metadata
from transform import Transform

def main():

    file_path = 'Code/data/cube.city.json' # Path to your CityJSON file
    file = open(file_path) # Open the provided cityjson file
    file_content_json = json.loads(file.read()) # Read the file as python dict 
    file_content_str = json.dumps(file_content_json) # Transform the python dict to python json string cijo validator requires a string
    file_content_keys = file_content_json.keys() # Get all first level keys in the python dict
    val = cjvalpy.CJValidator([file_content_str]) # Create a CJValidator object using the provided CityJSON data as a list of strings
    valid_city_json_file = val.validate() # Validate the CityJSON data using the CJValidator instance
    has_extension = "extensions" in file_content_keys # Check if the file contains extensions
    has_appearance = "appearance" in file_content_keys # Check if the file contains appearance
    has_geometry_templates = "geometry_templates" in file_content_keys # Check if the file contains geometry_templates

    # Check if the provided file is a valid cityjson file and doesn't have extensions, appearance, nor geometry templates
    if valid_city_json_file and not has_appearance and not has_extension and not has_geometry_templates:
        cityjson_data = cityjson.load(file_path) # Load the CityJSON data from the specified file path
        has_metadata = cityjson_data.has_metadata() # Check if the file has metadata

        if has_metadata:
            metadata_values = cityjson_data.get_metadata() # Extract metadata values from the loaded CityJSON data
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

            metadata_obj = Metadata(**constructor_args) # Create the Metadata object with the filtered arguments
            print(metadata_obj.to_json())

            print("\n")

            transform_values = file_content_json["transform"] # Extract transform values from the loaded CityJSON python dic
            scale = transform_values["scale"] # Extract scale values from the transform_values
            translate = transform_values["translate"] # Extract translate values from the transform_values
            transform_obj = Transform(scale=scale, translate=translate) #  Create the Transform object
            print(transform_obj.to_json())

            # Write JSON to file
            # with open('metadataLD.json', 'w') as json_file:
            #     json.dump(metadata_dict, json_file, indent=4, ensure_ascii=False)

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
    main()
