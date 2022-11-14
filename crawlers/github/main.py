import time
import json
import logging
import redis

from source.GithubCrawler import GithubCrawler
from source.utils.utils import Utils

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
"""
Init redis instance and crawler instance 
"""
config = Utils.load_json_file('config.json')
redis_cache = redis.Redis(host=config["redis"]["host"], port=config["redis"]["port"], db=0)
crawler = GithubCrawler(redis_cache=redis_cache)
logger.info("Crawler starting...")
while True:
    for keyword in config["keywords"]:
        try:
            crawler.crawl(keyword)
            crawler.update_redis(keyword)
        except:
            logger.info("Error when crawl with keyword: %s", keyword)

    time.sleep(config["delay"])

        



    
