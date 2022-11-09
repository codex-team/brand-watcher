import redis
from source.utils.log import logger


class CacheDB:
    '''Methods to work with Redis cache database'''

    def __init__(self, host: str, port: str, password: str = '') -> None:
        try:
            self.redis = redis.StrictRedis(
                host=host, port=port, password=password)
            logger.info(f'Connected to cache database on port: {port}')
        except Exception as e:
            logger.error(f'Error while connecting to cache database: {e}')

    def save_data(self, key: str, data: str) -> None:
        self.redis.set(key, data)

    def find_data(self, key: str) -> str:
        return self.redis.get(key)
