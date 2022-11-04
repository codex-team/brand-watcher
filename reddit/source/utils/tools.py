import json
import requests
import requests.auth
import config

def read_list():
    with open(config.keywords_path, 'r') as f:
        data = json.load(f)
        return data

def read_access_token():
    with open(config.token_path, "r") as f:
        data = json.load(f)
        return data


def save_access_token(creds):
    with open(config.token_path, "w") as f:
        json.dump(creds, f)


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
    response = requests.post(url=url, auth=client_auth, data=post_data, headers=headers)
    return response.json()


if __name__ == "__main__":
    access = get_access_token(config.USER_NAME, config.PASSWORD,
                        config.CLIENT_ID, config.CLIENT_SECRET)
    print(access)
