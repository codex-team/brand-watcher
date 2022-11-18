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

    def save_data(self, key: str, data: str):
        self.redis.set(key, data)

    def find_data(self, key: str) -> str:
        return self.redis.get(key)
