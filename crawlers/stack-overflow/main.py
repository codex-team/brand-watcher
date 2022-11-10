import time
import logging

from stackoverflow.stackoverflow import StackOverflowCrawler
from stackoverflow.utils.utils import Utils
from stackoverflow.db.db import Db

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    config = Utils.load_json_file('config.json')

    db = Db(config['redis']['host'], config['redis']['port'], config['redis']['password'])

    while True:
        crawler = StackOverflowCrawler(config['keywords'], db)
        crawler.crawl()
        time.sleep(config['delay'])

