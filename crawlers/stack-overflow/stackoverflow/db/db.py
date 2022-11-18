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

    def save_data(self, data_id, keyword, date):
        """
        Save data
        :param data_id: key for database
        :param keyword: keyword of founded data
        :param date: crawling data update date
        """

        self.redis.hset(f'{self.crawler_name}:{keyword}', data_id, date)

    def find_data(self, data_id, keyword):
        """
        Find data
        :param data_id: key for search
        :param keyword: keyword in founded data
        :returns founded data
        """

        return self.redis.hget(f'{self.crawler_name}:{keyword}', data_id)
