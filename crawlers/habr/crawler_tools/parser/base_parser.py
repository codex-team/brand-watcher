import logging
import requests
from bs4 import BeautifulSoup
from time import sleep

from crawler_tools.utils.utils import dict_to_json


class BaseParser:
    """The main parser on which other parsers can be based"""
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Accept': '*/*'
    }

    def __init__(self, db, params, page_delay=0):
        """
        :param db - cache Redis Database for repeats elimination,
        :param params - get-request parameters in URL,
        :param page_delay - delay by every request for blocking prevention
        """
        self.db = db
        self.params = params
        self.page_delay = page_delay

    @staticmethod
    def sleep(time):
        """Use for delay implementation"""
        sleep(time)

    def get_soup(self, url, params=None):
        """Return a html-tree by request. Using by every requests"""
        self.sleep(self.page_delay)
        try:
            if params is None:
                params = dict()
            req = requests.get(url, params=params, headers=self.HEADERS)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            return soup
        except requests.Timeout as err:
            logging.warning(f"Ошибка timeout, при запросе: {url}, error: ', {err}")
            return None
        except requests.HTTPError as err:
            code = err.response.status_code
            logging.warning(f"Ошибка при запросе: {url}, code: {code}")
            return None
        except requests.RequestException as err:
            logging.warning(f'Ошибка при запросе: {url} , {err}')
            return None

    def save_in_db(self, url, data):
        """Save info from request in redis"""
        string_result = dict_to_json(data)
        self.db.save_data(url, string_result)

    def post_handler(self, url, h1_class, meta_data_class, author_class, content_id, absence):
        """Base function for page parsing"""

        soup = self.get_soup(url, self.params)

        for cls in absence:
            expired_company = soup.find('div', class_=cls)
            if expired_company:
                logging.info(f'Article {url} is empty. Company is not available.')
                return {}

        title = soup.find('h1', class_=h1_class).text

        meta_data = soup.find('div', class_=meta_data_class)
        author = meta_data.find('span', class_=author_class).text.strip()
        data_published = meta_data.find('time')['datetime']

        text = soup.find('div', id=content_id).text

        result_dict = {
            'title': title,
            'URL': url,
            'author': author,
            'data_published': data_published,
            'text': text,
        }

        return result_dict


