import time
import logging

from stackoverflow.stackoverflow import StackOverflowCrawler
from stackoverflow.utils.utils import Utils
from stackoverflow.db.db import Db
from stackoverflow.broker.broker import Broker

logging.basicConfig(level=logging.DEBUG)

CRAWLER_NAME = 'stack-overflow'

if __name__ == '__main__':
    config = Utils.load_json_file('config.json')

    db = Db(config['redis-url'], CRAWLER_NAME)
    broker = Broker(config['rabbitmq-url'], CRAWLER_NAME)

    while True:
        crawler = StackOverflowCrawler(config['keywords'], db, broker)
        crawler.crawl()
        time.sleep(config['delay'])