import requests
import json
import redis 
import logging

from source.db.db import Db
from source.utils.utils import Utils

BASE_URL = "https://api.github.com/search/repositories"

"""
Crawler has 2 properties is base URL of GithubAPI 
and redis's database information.
"""

class GithubCrawler:

    def __init__(self, cache: Db, name: str = 'GithubCrawler' ):
        self.name = name
        self.cache = cache

    """
    Define crawl function, which accept keyword from
    config file and make request to github API to get 
    coresponding data.
    """

    def _save_to_cache(self, keyword, data):
        # Check if keyword already in cache or not
        for item in data:
            key = f'{self.name}:{keyword}'
            id = item['url']
            if not self.cache.is_existed(key, id):
                self.cache.add_to_set(key, id)

    def crawl(self, keyword):
        data = []
        rq = f'{BASE_URL}?q={keyword}' 
        response = requests.get(rq).json()
        if len(response) == 0:
            logging.info(f"No data match with keyword: {keyword}")
        else:
            items = response["items"]
            for i in range(len(items)):
                tmp = {}
                tmp["repo_full_name"] = items[i]["full_name"]
                tmp["url"] = items[i]["html_url"]
                tmp["owner"] = items[i]["owner"]["login"]
                tmp["description"] = items[i]["description"]
                tmp["language"] = items[i]["language"]
                data.append(tmp)

        self._save_to_cache(keyword, data)

        return data