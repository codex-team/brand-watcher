from crawler_tools.parser.habr_parser import HabrParser
from crawler_tools.utils.utils import load_json_file, save_parsing_data
from crawler_tools.redis_db.db import Db

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    config = load_json_file('config.json.sample')

    host, port, password = config['redis']['host'], config['redis']['port'], config['redis']['password']
    db = Db(host, port, password)
    db.clear_cache()

    while True:
        logging.info('Start parsing')
        habr_parser = HabrParser(db, config['keywords'], config['page_delay'])
        json_result = habr_parser.run_parser(config['required_page_number'])
        save_parsing_data(json_result)

        habr_parser.sleep(config['delay'])
