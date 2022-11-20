from crawler_tools.parser.habr_parser import HabrParser
from crawler_tools.utils.utils import load_json_file, add_or_save_data_to_json
from crawler_tools.redis_db.db import Db

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    config = load_json_file('config.json.sample')

    host, port, password = config['redis']['host'], config['redis']['port'], config['redis']['password']
    db = Db(host, port, password)
    db.clear_cache()

    while True:
        habr_parser = HabrParser(db, config['keywords'])
        result = habr_parser.run_parser(config['required_page_number'])
        if result is not None and len(result) > 0:
            # TODO How to add new data in result.json - file is very big to use json lib
            add_or_save_data_to_json(result, 'result.json')
        habr_parser.sleep(config['delay'])
