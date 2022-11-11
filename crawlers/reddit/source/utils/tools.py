import json
from pathlib import Path
from .log import logger

config_path = (Path(__file__).absolute().parent.parent.parent/'config.json')
data_path = (Path(__file__).absolute().parent.parent.parent/'data.json')


def read_config():
    with open(config_path, 'r') as f:
        data = json.load(f)
        return data


def read_list():
    with open(config_path, 'r') as f:
        data = json.load(f)
        return data.get('keywords')


def save_list(data):
    with open(data_path, 'w') as f:
        json.dump(data, f)