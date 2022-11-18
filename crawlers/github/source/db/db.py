import logging
import redis

class Db:
    """
    The Db has methods to work with database
    :param host - database host
    :param port - database port
    :param password - database password
    """

    def __init__(self, url: str):
        try:
            self.redis = redis.StrictRedis.from_url(url, decode_responses=True)
            
            logging.info(f'Connected to cache database on url: {url}')
        except Exception as e:
            logging.error(f'Error while connecting to cache database: {e}')
    
    def add_to_set(self, key: str, id: str):
        self.redis.sadd(key, id)
    
    def is_existed(self, key: str, id: str) -> bool:
        logging.info(f'Repo {id} is in dataset {key}: {self.redis.sismember(key, id)}')
        return self.redis.sismember(key, id)