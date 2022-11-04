from time import sleep
from source.crawlers.reddit import RedditCrawler
from source.utils.tools import get_access_token, save_access_token, read_list
import config
import json
import redis
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

cache_db = redis.Redis(host=config.redis_creds["host"],
                       port=config.redis_creds["port"], db=0, password=config.redis_creds["password"])

try:
    crawler = RedditCrawler(cache_db)
    id = crawler.identify()
    logger.info(
        f'Logged in under account: {id["subreddit"]["title"]}|{id["subreddit"]["display_name_prefixed"]}')
except:
    logger.info('Account is not logged in ! Initiate login ...')
    response = get_access_token(
        config.USER_NAME, config.PASSWORD, config.CLIENT_ID, config.CLIENT_SECRET)
    access_token = response['access_token']
    save_access_token(access_token)
    crawler = RedditCrawler(cache_db)
    id = crawler.identify()
    logger.info(
        f'Logged in under account: {id["subreddit"]["title"]}|{id["subreddit"]["display_name_prefixed"]}')

logger.info("Start crawling ...")

while True:
    keywords = read_list()
    result = {}
    for keyword in keywords:
        result[keyword] = crawler.hot_posts(keyword)

    with open(config.data_path, 'w') as f:
        json.dump(result, f)

    sleep(1)
