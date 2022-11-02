from time import sleep
from source.crawlers.reddit import RedditCrawler
from source.utils.config import get_access, read, save, read_list
import json
import redis

query_str = "crawl"
data_path = "data.json"
cache_db = redis.Redis(host='redis-10381.c135.eu-central-1-1.ec2.cloud.redislabs.com',
                       port=10381, db=0, password='EcqJqZRW8CPeSWaSvBpmN4vOpIh2tXoZ')

try:
    crawler = RedditCrawler(cache_db)
    id = crawler.identify()
    print(
        f'Logged in under account: {id["subreddit"]["title"]}|{id["subreddit"]["display_name_prefixed"]}')
except:
    print('Account is not logged in ! Initiate login ...')
    creds = read()
    response = get_access(
        creds['USER_NAME'], creds['PASSWORD'], creds['CLIENT_ID'], creds['CLIENT_SECRET'])
    creds['ACCESS_TOKEN'] = response['access_token']
    save(creds)
    crawler = RedditCrawler(cache_db)
    id = crawler.identify()
    print(
        f'Logged in under account: {id["subreddit"]["title"]}|{id["subreddit"]["display_name_prefixed"]}')

print("Start crawling ...")

while True:
    keywords = read_list()
    result = {}
    for keyword in keywords:
        result[keyword] = crawler.hot_posts(keyword)

    with open(data_path, 'w') as f:
        json.dump(result, f)

    sleep(1)
