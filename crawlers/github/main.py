import time
import json
import logging
import redis

from source.GithubCrawler import GithubCrawler
from source.utils.utils import Utils
from source.db.db import Db
from source.broker.message_queue import Broker

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
"""
Init redis instance and crawler instance 
"""
if __name__ == '__main__':

    config = Utils.load_json_file('config.json')

    db = Db(config['redis_url'], crawler_name='github')

    broker = Broker(config['rabbitmq-url'], queue_name='github')

    crawler = GithubCrawler(cache=db, broker=broker)

    logger.info('Crawler starting...')

    while True:
        result = {}
        for keyword in config['keywords']:
            result[keyword] = crawler.crawl(keyword)

        time.sleep(config['delay'])
