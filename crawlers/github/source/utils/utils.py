import json 
from pathlib import Path 
from hashlib import sha256

config_path = (Path(__file__).absolute().parent.parent.parent/'config.json')

class Utils:
    """
    Utils contains helpers
    """
    # Read config file
    @staticmethod
    def load_json_file(file_path):
        """
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