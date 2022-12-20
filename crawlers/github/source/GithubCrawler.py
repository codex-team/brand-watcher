import requests
import json
import redis
import logging

from source.db.db import Db
from source.utils.utils import Utils
from source.broker.message_queue import Broker
BASE_URL = 'https://api.github.com/search/repositories'

"""
Crawler has 2 properties is base URL of GithubAPI 
and redis's database information.
"""


class GithubCrawler:

    def __init__(self, cache: Db, broker: Broker, name: str = 'GithubCrawler'):
        '''
        :param `name`: name of crawler
        :param `cache`: redis database
        '''
        self.name = name
        self.cache = cache

    def _save_to_cache(self, keyword, item):
        ''' Check if keyword already in cache or not. If not, then update

        :param `keyword`: keyword from config file to get the realated data
        :param `data`: the data we got after make request
        '''
        key = f'{self.name}:{keyword}'
        id = Utils.hash_data(item['url'])
        if not self.cache.is_existed(key, id):
            self.cache.add_to_set(key, id, item['date'])

    def crawl(self, keyword):
        ''' Make request to github API in order to crawl related data with keyword

        :param `keyword`: keyword from config file to get the related data
        '''
        data = []
        rq = f'{BASE_URL}?q={keyword}'
        response = requests.get(rq).json()
        if len(response) == 0:
            logging.info(f'No data match with keyword: {keyword}')
        else:
            items = response["items"]
            '''
            Pasre raw data to usefull data
            `repo_full_name`: name of repository in github
            `url`: html url of the repository
            `owner`: repository's owner 
            `description`: description about repository
            `language`: language is used to written repository          
            '''
            for item in items:
                tmp = {}
                tmp['repo_full_name'] = item['full_name']
                tmp['url'] = item['html_url']
                tmp['owner'] = item['owner']['login']
                tmp['description'] = item['description']
                tmp['language'] = item['language']
                tmp['date'] = item['created_at']
                data.append(tmp)

                self._save_to_cache(keyword, tmp)

                self.broker.send(json.dumps(tmp))

        return data
