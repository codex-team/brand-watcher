import time
import json
import logging
import redis

from source.GithubCrawler import GithubCrawler
from source.utils.utils import Utils
from source.db.db import Db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
"""
Init redis instance and crawler instance 
"""
if __name__ == '__main__':
    config = Utils.load_json_file('config.json')

    db = Db(config['redis']['host'], config['redis']['port'], config['redis']['password'])
    
    logger.info("Crawler starting...")

    while True:
        crawler = GithubCrawler(db=db)
        for keyword in config["keywords"]:
            try:
                crawler.crawl(keyword)
                crawler.update_redis(keyword)
            except:
                logger.info("Error when crawl with keyword: %s", keyword)

        time.sleep(config["delay"])

        



    
