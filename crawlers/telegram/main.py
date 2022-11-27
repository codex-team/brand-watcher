import asyncio

from telegram.utils.utils import Utils
from telegram.crawler import TelegramCrawler
from telegram.db.db import Db
from telegram.broker.broker import Broker

CRAWLER_NAME = "telegram"


async def main():
    config = Utils.load_json_file('config.json')
    db = Db(config['redis-url'], CRAWLER_NAME)
    broker = Broker(config['rabbitmq-url'], CRAWLER_NAME)

    # Create callback for new data
    async def callback(message: str):
        broker.send(message)

    crawler = TelegramCrawler(config['keywords'], config['telegram']['chats'], callback, config['telegram']['api_id'],
                              config['telegram']['api_hash'], config['session_name'], db)

    await crawler.start()


asyncio.run(main())
