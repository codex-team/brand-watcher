from crawler_tools.habr_parser import HabrParser
from crawler_tools.utils.utils import Utils
from crawler_tools.redis_db.db import Db

# TODO make code review
# TODO add logging

if __name__ == '__main__':
    config = Utils.load_json_file('config.json.sample')
    host, port, password = config['redis']['host'], config['redis']['port'], config['redis']['password']
    db = Db(host, port, password)

    while True:
        habr_parser = HabrParser(db, config['keywords'])
        result = habr_parser.run_parser(config['num'])
        if result:
            with open('result', 'a') as f:
                f.write(result)

        habr_parser.sleep(config['delay'])
