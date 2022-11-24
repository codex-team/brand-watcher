import redis
from source.utils.log import logger


class CacheDB:
    '''Methods to work with Redis cache database'''

    def __init__(self, url: str):
        try:
            self.redis = redis.StrictRedis.from_url(url, decode_responses=True)
            logger.info(f'Connected to cache database on url: {url}')
        except Exception as e:
            logger.error(f'Error while connecting to cache database: {e}')

    def add_to_set(self, key, id, date):
        self.redis.hset(id, key, date)

    def find_date(self, key: str, id: str) -> str:
        logger.info(f'Article {id} of {key} created at date: {self.redis.hget(id, key)}')
        return self.redis.hget(id, key)
