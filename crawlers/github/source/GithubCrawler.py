import requests
import json
import redis 
import logging

BASE_URL = "https://api.github.com/search/repositories"

"""
Crawler has 2 properties is base URL of GithubAPI 
and redis's database information.
"""

class GithubCrawler:
    def __init__(self, redis_cache):
        self.base_url = BASE_URL
        self.redis_cache = redis_cache
    """
    Define crawl function, which accept keyword from
    config file and make request to github API to get 
    coresponding data.
    """
    def crawl(self, keyword):
        data = []
        try:
            rq = self.base_url+ "?" + "q=" + keyword 
            response = requests.get(rq).json()
        except:
            logging.info("Error when make request to Github API")
        if len(response) == 0:
            logging.info("No data match with this keyword")
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
        return data
    """
    Update keyword into redis if coresponding data haven't exits
    """
    def update_redis(self, keyword):
        if not self.redis_cache.exists(keyword):
            self.redis_cache.set(keyword, str(self.crawl(keyword)))
    
            

            

        
