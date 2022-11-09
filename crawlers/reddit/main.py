from time import sleep
from source.database.cache import CacheDB
from source import RedditCrawler
from source.utils.tools import read_list, read_config, save_list
from source.utils.log import logger

redis_creds = read_config().get('redis_creds')

cache_db = CacheDB(host=redis_creds["host"],
                   port=redis_creds["port"], password=redis_creds["password"])

crawler = RedditCrawler(cache_db)

logger.info("Start crawling ...")

while True:
    keywords = read_list()
    result = {}
    for keyword in keywords:
        result[keyword] = crawler.hot_posts(keyword)

    save_list(result)

    sleep(1)
