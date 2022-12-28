from crawler_tools.parser.habr_parser import HabrParser
from crawler_tools.utils.utils import load_json_file
from crawler_tools.redis_db.db import Db
from crawler_tools.broker.broker import Broker

import logging
from time import sleep
logging.basicConfig(level=logging.DEBUG)

CRAWLER_NAME = 'habr'

if __name__ == '__main__':
    config = load_json_file('config.json.sample')

    db = Db(config['redis-url'], CRAWLER_NAME)
    db.clear_cache()
    broker = Broker(config['rabbitmq-url'], CRAWLER_NAME)

    keywords = config['keywords']
    while True:
        for keyword in keywords:
            logging.info(f'Start parsing for @{keyword}@')
            habr_parser = HabrParser(db, keyword, broker, config['page_delay'])
            json_result = habr_parser.run_parser(config['required_page_number'])

        sleep(config['delay'])
