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


def json_result_name_time():
    """Return filename for parsing example"""
    current_time = datetime.now().time()
    return '%d:%d:%d.result.json' % (current_time.hour, current_time.minute, current_time.second)


def save_parsing_data(result):
    """Save result.json to file"""
    if result is not None and len(result) > 0:
        path = json_result_name_time()
        with open(path, 'w') as file:
            file.write(result)
