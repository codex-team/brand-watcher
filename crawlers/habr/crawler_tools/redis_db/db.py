import logging
import redis


class Db:
    """
    The Db has methods to work with database
    :param url - database url for connection
    """
    def __init__(self, url, crawler_name):
        self.crawler_name = crawler_name
        try:
            self.redis = redis.Redis.from_url(url)
            logging.info(f'Connected to database on: {url}')
        except Exception as e:
            logging.error(f'Error while connecting to database: {e}')

    def save_data(self, data_id, keyword, data: str):
        """
        Save data
        :param keyword: keyword of founded data
        :param data_id: key for database
        :param data: data to save
        """

        self.redis.hset(f'{self.crawler_name}:{keyword}', data_id, data)

    def find_data(self, data_id, keyword):
        """
        Find data
        :param keyword: keyword of founded data
        :param data_id: key for search
        :returns founded object
        """

        return self.redis.hget(f'{self.crawler_name}:{keyword}', data_id)

    def clear_cache(self):
        """Clear existing cache"""
        self.redis.flushdb()
