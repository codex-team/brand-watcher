import json
import requests
import requests.auth
from pathlib import Path
from .log import logger

config_path = (Path(__file__).absolute().parent.parent.parent/'config.json')
data_path = (Path(__file__).absolute().parent.parent.parent/'data.json')

def read_config():
    with open(config_path, 'r') as f:
        data = json.load(f)
        return data

def save_list(data):
    with open(data_path, "w") as f:
        json.dump(data, f)


def read_list():
    with open(config_path, 'r') as f:
        data = json.load(f)
        return data.get('keywords')


def read_access_token():
    with open(config_path, "r") as f:
        data = json.load(f)
        return data.get('access_token')


def update_config(**kwargs):
    '''Update config file
    params must be specify'''
    conf = read_config()

    for key in kwargs.keys():
        if key in conf.keys():
            conf[key] = kwargs[key]

    with open(config_path, "w") as f:
        json.dump(conf, f)


def get_access_token(username, password, client_id, client_secret):
    url = "https://www.reddit.com/api/v1/access_token"
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    headers = {
        'User-agent': f'{username}/0.1'
    }
    response = requests.post(url=url, auth=client_auth,
                             data=post_data, headers=headers)
    access_token = response.json().get('access_token')
    if not access_token:
        logger.error('Login failed!!!')
        raise Exception('Login failed')

    return access_token
