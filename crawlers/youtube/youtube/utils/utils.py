import json
from hashlib import sha256


class Utils:
    """
    The Utils contains helpers
    """

    @staticmethod
    def load_json_file(file_path: str) -> dict:
        """
        Load json file
        :param file_path: path to json file
        :returns: json converted to dict
        """

        file = open(file_path)

        return json.load(file)

    @staticmethod
    def hash_data(data: str) -> str:
        """
        Make hash from string
        :param data: data to make hash
        :returns: hashed string
        """

        return sha256(data.encode('utf-8')).hexdigest()
