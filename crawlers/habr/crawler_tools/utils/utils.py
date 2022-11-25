import json
from datetime import datetime


def dict_to_json(data: dict):
    """Transfer python dict object to json"""
    return json.dumps(data, ensure_ascii=False)


def load_json_file(file_path: str) -> dict:
    """
    Load json file
    :param file_path: path to json file
    :returns: json converted to dict
    """

    file = open(file_path)

    return json.load(file)

