import json


def dict_to_json(data: dict):
    return json.dumps(data, ensure_ascii=False)


def load_json_file(file_path: str) -> dict:
    """
    Load json file
    :param file_path: path to json file
    :returns: json converted to dict
    """

    file = open(file_path)

    return json.load(file)


def add_or_save_data_to_json(input_json_data, path: str):
    input_dict_data = json.loads(input_json_data)

    with open(path, 'a+') as file:
        file.seek(0)
        json_data = file.read()
        python_dict = json.loads(json_data) if json_data else {}
        python_dict.update(input_dict_data)

        new_json_data = dict_to_json(python_dict)
        file.write(new_json_data)

