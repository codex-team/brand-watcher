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

    def __init__(self, cache: CacheDB, reddit: RedditAuth):
        self.cache = cache
        self.reddit = reddit

    def _get_from_cache(self, url: str, params: dict) -> dict:
        key = url + json.dumps(params)
        value = self.cache.find_data(key)
        if value:
            return json.loads(self.cache.find_data(key))

    def _save_to_cache(self, url: str, params: dict, value: dict):
        key = url + json.dumps(params)
        self.cache.save_data(key, json.dumps(value))

    @reddit_authenticated
    def identify(self) -> dict:
        '''Get identify of current Crawler user

        :return `dict` object
        '''
        url = f'{BASE_URL}api/v1/me'
        response = requests.get(url, headers=self.reddit.headers).json()

        return response

    @reddit_authenticated
    def subreddit(self, query: str, exact: bool = False, include_over_18: bool = True, include_unadvertisable: bool = True, search_query_id: str = None, typeahead_active: bool = None) -> list:
        '''List subreddit names that begin with a query string

        :param `exact`: boolean 
        :param `include_over_18`: boolean 
        :param `include_unadvertisable`: boolean 
        :param `query`: a string up to 50 characters long, consisting of printable characters.
        :param `search_query_id`: an uuid
        :param `typeahead_active`: boolean value or None
        :return `list` type

        Subreddits whose names begin with `query` will be returned. If `include_over_18` is false, subreddits with over-18 content restrictions will be filtered from the results.

        If `include_unadvertisable` is False, subreddits that have `hide_ads` set to True or are on the `anti_ads_subreddits` list will be filtered.

        If `exact` is true, only an exact match will be returned. Exact matches are inclusive of `over_18 subreddits`, but not `hide_ad` subreddits when `include_unadvertisable` is False.
        '''
        url = f'{BASE_URL}api/search_reddit_names'
        params = {
            'exact': exact,
            'include_over_18': include_over_18,
            'include_unadvertisable': include_unadvertisable,
            'query': query,
            'search_query_id': search_query_id,
            'typeahead_active': typeahead_active
        }
        response = self._get_from_cache(url, params)

        if not response:
            response = requests.get(
                url, params=params, headers=self.reddit.headers).json()['names']
            self._save_to_cache(url, params, response)

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
        data = self._get_from_cache(url, params)

        if not data:
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
            self._save_to_cache(url, params, data)

        return data