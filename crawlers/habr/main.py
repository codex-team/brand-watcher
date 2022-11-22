from crawler_tools.parser.habr_parser import HabrParser
from crawler_tools.utils.utils import load_json_file, save_parsing_data
from crawler_tools.redis_db.db import Db

import logging
from time import sleep
logging.basicConfig(level=logging.DEBUG)

CRAWLER_NAME = 'habr'

if __name__ == '__main__':
    config = load_json_file('config.json.sample')

    db = Db(config['redis-url'], CRAWLER_NAME)
    db.clear_cache()

    keywords = config['keywords']
    while True:
        for keyword in keywords:
            logging.info(f'Start parsing for @{keyword}@')
            habr_parser = HabrParser(db, keyword, config['page_delay'])
            json_result = habr_parser.run_parser(config['required_page_number'])
            save_parsing_data(json_result, keyword)

        sleep(config['delay'])
