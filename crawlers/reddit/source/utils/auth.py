import requests
from .log import logger


class RedditAuth:
    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.authenticate()

    def _get_access_token(self):
        url = 'https://www.reddit.com/api/v1/access_token'
        client_auth = requests.auth.HTTPBasicAuth(
            self.client_id, self.client_secret)
        post_data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }
        headers = {
            'User-agent': f'{self.username}/0.1'
        }
        response = requests.post(url=url, auth=client_auth,
                                 data=post_data, headers=headers)
        access_token = response.json().get('access_token')
        if not access_token:
            logger.error('Login failed!!!')
            raise Exception('Login failed')

        return access_token

    def check_login(self):
        url = f'https://oauth.reddit.com/api/v1/me'

        response = requests.get(url, headers=self.headers).json()

        if response.get('subreddit'):
            logger.info(
                f"Logged in under account: {response['subreddit']['title']}|{response['subreddit']['display_name_prefixed']}")
            return True

        logger.info("Account is not logged in!!!")
        return False

    def authenticate(self):
        self.access_token = self._get_access_token()
        self.headers = {
            'Authorization': 'bearer ' + self.access_token,
            'User-agent': self.username + '/0.1',
        }

        if not self.check_login():
            raise Exception("Login failed")
