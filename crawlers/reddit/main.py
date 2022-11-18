from time import sleep
from source.database.cache import CacheDB
from source import RedditCrawler
from source.utils.tools import read_list, read_config, save_list
from source.utils.log import logger
from source.utils.auth import RedditAuth

if __name__ == '__main__':

    config = read_config()

    reddit_auth = RedditAuth(
        config['client_id'], config['client_secret'], config['username'], config['password'])

    cache_db = CacheDB(config['redis_url'])

    crawler = RedditCrawler(cache_db, reddit_auth)

    logger.info('Start crawling ...')

    while True:
        keywords = read_list()
        result = {}
        for keyword in keywords:
            result[keyword] = crawler.hot_posts(keyword)

        sleep(config.get('delay', 30))
