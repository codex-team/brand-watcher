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

    def add_to_set(self, key: str, id: str):
        self.redis.sadd(key, id)

    def is_existed(self, key: str, id: str) -> bool:
        logger.info(f'Article {id} is in dataset {key}: {self.redis.sismember(key, id)}')
        return self.redis.sismember(key, id)
