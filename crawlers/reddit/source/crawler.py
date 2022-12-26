import requests
import requests.auth
import json
from source.database.cache import CacheDB
from source.broker import Broker
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

    def __init__(self, cache: CacheDB, reddit: RedditAuth, broker: Broker, name: str = 'RedditCrawler'):
        self.name = name
        self.cache = cache
        self.reddit = reddit
        self.broker = broker

    def _save_to_cache(self, keyword, article):
        '''Check for existance and save to cache'''
        key = f'{self.name}:{keyword}'
        id_hash = hash(article['id'])
        date = article['date']
        if not self.cache.find_date(key, id_hash):
            self.cache.add_to_set(key, id_hash, date)

    @reddit_authenticated
    def identify(self) -> dict:
        '''Get identify of current Crawler user

        :return `dict` object
        '''
        url = f'{BASE_URL}api/v1/me'
        response = requests.get(url, headers=self.reddit.headers).json()

        return response

    @reddit_authenticated
    def comments(self, subreddit: str, article_id: str) -> list:
        '''Get list of comments from article'''
        url = f'{BASE_URL}r/{subreddit}/comments/{article_id}'
        response = requests.get(url, headers=self.reddit.headers).json()

        return [cmt['data']['body'] for cmt in response[1]['data']['children']]

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

        response = requests.get(
            url, params=params, headers=self.reddit.headers)
        articles = response.json()['data']['children']
        data = []
        for article in articles:
            tmp = article['data']
            article_details = {
                'title': tmp['title'],
                'comments': self.comments(subreddit, tmp['id']),
                'date': tmp['created_utc'],
                'source': self.name,
                'url': tmp['url'],
                'keyword': subreddit,
            }

            self.broker.send(json.dumps(article_details))
            self._save_to_cache(subreddit, article_details)
            data.append(article_details)

        return data
