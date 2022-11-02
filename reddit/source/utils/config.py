import json
import requests
import requests.auth
from CONFIG import creds_path, keywords_path

def read_list():
    with open(keywords_path, 'r') as f:
        data = json.load(f)
        return data

def read():
    with open(creds_path, "r") as f:
        data = json.load(f)
        return data


def save(creds):
    with open(creds_path, "w") as f:
        json.dump(creds, f)


def get_access(username, password, client_id, client_secret):
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
    creds = read()
    access = get_access(creds["USER_NAME"], creds["PASSWORD"],
                        creds["CLIENT_ID"], creds["CLIENT_SECRET"])
    print(access)
