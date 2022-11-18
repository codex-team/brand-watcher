import requests
import requests.auth
import json
from source.database.cache import CacheDB
from source.utils.log import logger
from source.utils.auth import RedditAuth
from source.utils.tools import hash
from functools import wraps

BASE_URL = 'https://oauth.reddit.com/' 

def reddit_authenticated(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.error(f'Crawler Error: {e}')
            self.reddit.authenticate()
            return func(self, *args, **kwargs)

    return wrapper  


class RedditCrawler:

    def __init__(self, cache: CacheDB, reddit: RedditAuth, name: str = 'RedditCrawler'):
        self.name = name
        self.cache = cache
        self.reddit = reddit

    def _save_to_cache(self, keyword, data):
        '''Check for existance and save to cache'''
        for article in data:
            key = f'{self.name}:{keyword}'
            id = article['id']
            if not self.cache.is_existed(key, id):
                self.cache.add_to_set(key, id)

    @reddit_authenticated
    def identify(self) -> dict:
        '''Get identify of current Crawler user

        :return `dict` object
        '''
        url = f'{BASE_URL}api/v1/me'
        response = requests.get(url, headers=self.reddit.headers).json()

        return response

    @reddit_authenticated
    def hot_posts(self, subreddit: str, g: str = 'GLOBAL', after: str = None, before: str = None, count: int = 0, limit: int = 25, show: str = None, sr_detail: str = None) -> list:
        '''List hotest posts from specific subreddit

        :param `g`: one of (GLOBAL, US, AR, ...)
        :param `after`: fullname of a thing
        :param `befor`: fullname of a thing
        :param `count`: a positive integer (default: 0)
        :param `limit`: the maximum number of items desired (default: 25, maximum: 100)
        :param `show`: (optional) the string all
        :param `sr_detail`: (optional) expand subreddits
        :return `dict` type
        '''
        url = f'{BASE_URL}r/{subreddit}/hot'
        params = {
            'g': g,
            'after': after,
            'before': before,
            'count': count,
            'limit': limit,
            'show': show,
            'sr_detail': sr_detail
        }

        response = requests.get(url, params=params, headers=self.reddit.headers)
        articles = response.json()['data']['children']
        data = []
        for article in articles:
            tmp = article['data']
            data.append({
                'id': tmp['id'],
                'title': tmp['title'],
                'author': tmp['author'],
                'url': tmp['url'],
                'tag': tmp['link_flair_text'],
                'num_cmt': tmp['num_comments']
            })

        self._save_to_cache(subreddit, data)

        return data