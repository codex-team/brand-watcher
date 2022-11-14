import time
import logging

from youtube.youtube import YouTubeCrawler
from youtube.utils.utils import Utils
from youtube.db.db import Db

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    config = Utils.load_json_file('config.json')

    db = Db(config['redis']['host'], config['redis']['port'], config['redis']['password'])

    while True:
        crawler = YouTubeCrawler(config['keywords'], db, config['api_key'])
        crawler.crawl()
        time.sleep(config['delay'])

