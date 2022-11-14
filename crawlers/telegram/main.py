import asyncio

from telegram.utils.utils import Utils
from telegram.crawler import TelegramCrawler


async def main():
    config = Utils.load_json_file('config.json.sample')
    crawler = TelegramCrawler(config['keywords'], config['telegram']['chats'], config['telegram']['api_id'],
                              config['telegram']['api_hash'], config['session_name'], config['redis-url'],
                              config['rabbitmq-url'])

    await crawler.start()


asyncio.run(main())
