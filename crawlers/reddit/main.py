from time import sleep
from source.database.cache import CacheDB
from source.broker import Broker
from source import RedditCrawler
from source.utils.tools import read_list, read_config
from source.utils.log import logger
from source.utils.auth import RedditAuth

CRAWLER_NAME = 'reddit'

if __name__ == '__main__':

    config = read_config()

    reddit_auth = RedditAuth(
        config['client_id'], config['client_secret'], config['username'], config['password'])

    cache_db = CacheDB(config['redis_url'])
    broker = Broker(config['rabbitmq_url'], CRAWLER_NAME)

    crawler = RedditCrawler(cache_db, reddit_auth, broker, CRAWLER_NAME)

    logger.info('Start crawling ...')

    while True:
        keywords = read_list()
        result = {}
        for keyword in keywords:
            result[keyword] = crawler.hot_posts(keyword)

        sleep(config.get('delay', 30))
