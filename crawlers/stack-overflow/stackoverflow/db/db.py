import json
import logging

import redis


class Db:
    """
    The Db has methods to work with database
    :param url - database url for connection
    :param crawler_name - name of crawler
    """

    def __init__(self, url, crawler_name):
        self.crawler_name = crawler_name
        try:
            self.redis = redis.StrictRedis.from_url(url, decode_responses=True)
            logging.info(f'Connected to database on: {url}')
        except Exception as e:
            logging.error(f'Error while connecting to database: {e}')

    def save_data(self, data_id, keyword):
        """
        Save data
        :param data_id: key for database
        :param keyword: keyword of founded data
        """

        data = []

        # Get data from redis by keyword
        redis_hash = self.redis.hget(self.crawler_name, keyword)

        # Check if data by keyword exists
        if redis_hash:
            data = json.loads(redis_hash)

        # Add new data id
        data.append(data_id)

        str_data = json.dumps(data)

        # Save updated data
        self.redis.hset(self.crawler_name, keyword, str_data)

    def find_data(self, data_id, keyword) -> bool:
        """
        Find data
        :param data_id: key for search
        :param keyword: keyword in founded data
        :returns true if data was found
        """

        redis_hash = self.redis.hget(self.crawler_name, keyword)

        if redis_hash:
            if data_id in json.loads(redis_hash):
                return True

        return False
