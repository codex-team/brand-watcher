import logging

import redis


class Db:
    """
    The Db has methods to work with database
    :param host - database host
    :param port - database port
    :param password - database password
    """

    def __init__(self, redis_url):
        try:
            self.redis = redis.Redis.from_url(redis_url)
            logging.info(f'Connected to database on: {redis_url}')
        except Exception as e:
            logging.error(f'Error while connecting to database: {e}')

    def save_data(self, data_id, data: str):
        """
        Save data
        :param data_id: key for database
        :param data: data to save
        """

        self.redis.set(data_id, data)

    def find_data(self, data_id):
        """
        Find data
        :param data_id: key for search
        :returns founded object
        """

        return self.redis.get(data_id)
