import json 

class Utils:
    """
    Utils contains helpers
    """
    @staticmethod
    def load_json_file(file_path):
        """
        :param file_path: path to json file
        :returns: json converted to dict
        """

        file = open(file_path)
        return json.load(file)
    