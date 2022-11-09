import requests
import requests.auth
import json
from source.database.cache import CacheDB
from source.utils.tools import read_access_token, get_access_token, update_config, read_config
from source.utils.log import logger


class RedditCrawler:

    def __init__(self, cache: CacheDB) -> None:
        self.cache = cache
        self.access_token = read_access_token()
        self.base_url = "https://oauth.reddit.com/"
        self.conf = read_config()
        self.headers = {
            "Authorization": "bearer " + self.access_token,
            "User-agent": self.conf["USER_NAME"] + "/0.1",
        }

    def _check_login(self) -> bool:
        '''Check if this instance is logged in'''
        id = self.identify()

        if id.get('subreddit'):
            logger.info(
                f'Logged in under account: {id["subreddit"]["title"]}|{id["subreddit"]["display_name_prefixed"]}')
            return True

        return False

    def _update_access_token(self) -> None:

        access_token = get_access_token(
            self.conf["USER_NAME"], self.conf["PASSWORD"], self.conf["CLIENT_ID"], self.conf["CLIENT_SECRET"])

        update_config(access_token=access_token)

        self.conf = read_config()
        self.headers = {
            "Authorization": "bearer " + self.access_token,
            "User-agent": self.conf["USER_NAME"] + "/0.1",
        }

    def _login(self) -> None:
        '''Login to Reddit API services
        If failed, get new access token and try again'''

        if not self._check_login():
            logger.info('Account is not logged in ! Initiate login ...')

            self._update_access_token()

            if not self._check_login():
                logger.error('Login failed!!!')
                raise Exception('Login failed')

    def _get_from_cache(self, url: str, params: dict) -> dict:
        key = url + json.dumps(params)
        value = self.cache.find_data(key)
        if value:
            return json.loads(self.cache.find_data(key))

    def _save_to_cache(self, url: str, params: dict, value: dict) -> None:
        key = url + json.dumps(params)
        self.cache.save_data(key, json.dumps(value))

    def identify(self) -> dict:
        '''Get identify of current Crawler user

        :return `dict` object
        '''
        url = f"{self.base_url}api/v1/me"
        response = requests.get(url, headers=self.headers).json()

        return response

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
        url = f"{self.base_url}api/search_reddit_names"
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
                url, params=params, headers=self.headers).json()['names']
            self._save_to_cache(url, params, response)

        return response

    def hot_posts(self, subreddit: str, g: str = "GLOBAL", after: str = None, before: str = None, count: int = 0, limit: int = 25, show: str = None, sr_detail: str = None) -> list:
        '''List hotest posts from specific subreddit

        :param `g`: one of (GLOBAL, US, AR, AU, BG, CA, CL, CO, HR, CZ, FI, FR, DE, GR, HU, IS, IN, IE, IT, JP, MY, MX, NZ, PH, PL, PT, PR, RO, RS, SG, ES, SE, TW, TH, TR, GB, US_WA, US_DE, US_DC, US_WI, US_WV, US_HI, US_FL, US_WY, US_NH, US_NJ, US_NM, US_TX, US_LA, US_NC, US_ND, US_NE, US_TN, US_NY, US_PA, US_CA, US_NV, US_VA, US_CO, US_AK, US_AL, US_AR, US_VT, US_IL, US_GA, US_IN, US_IA, US_OK, US_AZ, US_ID, US_CT, US_ME, US_MD, US_MA, US_OH, US_UT, US_MO, US_MN, US_MI, US_RI, US_KS, US_MT, US_MS, US_SC, US_KY, US_OR, US_SD)
        :param `after`: fullname of a thing
        :param `befor`: fullname of a thing
        :param `count`: a positive integer (default: 0)
        :param `limit`: the maximum number of items desired (default: 25, maximum: 100)
        :param `show`: (optional) the string all
        :param `sr_detail`: (optional) expand subreddits
        :return `dict` type
        '''
        url = f"{self.base_url}r/{subreddit}/hot"
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
            response = requests.get(url, params=params, headers=self.headers)
            articles = response.json()['data']['children']
            data = []
            for article in articles:
                tmp = article['data']
                data.append({
                    'title': tmp['title'],
                    'author': tmp['author'],
                    'url': tmp['url'],
                    'tag': tmp['link_flair_text'],
                    'num_cmt': tmp['num_comments']
                })
            self._save_to_cache(url, params, data)

        return data


if __name__ == "__main__":
    crawler = RedditCrawler()
    # print(crawler.identify())
    # print(crawler.subreddit(False, include_over_18=True,
    #       include_unadvertisable=True, query="python"))
    print(crawler.hot_posts('python', limit=10))
