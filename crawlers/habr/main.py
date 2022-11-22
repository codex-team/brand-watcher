from crawler_tools.parser.habr_parser import HabrParser
from crawler_tools.utils.utils import load_json_file, save_parsing_data
from crawler_tools.redis_db.db import Db

import logging
logging.basicConfig(level=logging.DEBUG)

CRAWLER_NAME = 'habr'

if __name__ == '__main__':
    # keyword is given in config["headers"]["q"]
    config = load_json_file('config.json.sample')

    db = Db(config['redis-url'], CRAWLER_NAME)
    db.clear_cache()

    while True:
        logging.info('Start parsing')
        habr_parser = HabrParser(db, config['headers'], config['page_delay'])
        json_result = habr_parser.run_parser(config['required_page_number'])
        save_parsing_data(json_result)

        habr_parser.sleep(config['delay'])
