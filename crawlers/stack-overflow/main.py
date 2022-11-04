import time
import logging

from stackoverflow.stackoverflow import StackOverflowCrawler
from stackoverflow.utils.utils import Utils

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    config = Utils.load_json_file('config.json.sample')

    while True:
        crawler = StackOverflowCrawler(config['keywords'], config['redis']['host'], config['redis']['port'],
                                       config['redis']['password'])
        crawler.crawl()
        time.sleep(config['delay'])

