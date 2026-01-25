import json


def parse_json(file_path):
    """
    Parses the data in a JSON file.

    Args:
        file_path (str):
            The path to the JSON file.

    Returns:
        dict:
            The data contained in the JSON file.
    """
    with open(file_path, "r") as json_file:
        return json.load(json_file)
