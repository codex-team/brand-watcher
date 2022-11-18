import json
from pathlib import Path
from hashlib import sha256
from .log import logger

config_path = (Path(__file__).absolute().parent.parent.parent/'config.json')
data_path = (Path(__file__).absolute().parent.parent.parent/'data.json')


def read_config() -> dict:
    '''Read Config file'''
    with open(config_path, 'r') as f:
        data = json.load(f)
        return data


def read_list() -> list:
    '''Read keywords list'''
    with open(config_path, 'r') as f:
        data = json.load(f)
        return data.get('keywords')


def save_list(data):
    '''Save data to data.json'''
    with open(data_path, 'w') as f:
        json.dump(data, f)


def hash(data) -> str:
    '''Make hash from string'''
    return sha256(data.encode('utf-8')).hexdigest()
