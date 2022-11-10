import asyncio

from crawler.utils.utils import Utils
from crawler.crawler import TelegramCrawler

KEYWORDS = ['editor.js', 'CodeX']
TELEGRAM_PUBLIC = ['habr_com', 'slaveeks_test_channel', 'test_chat_test_slaveeks']


async def callback(message):
    print(message)


async def main():
    config = Utils.load_json_file('config.json.sample')
    crawler = TelegramCrawler(config['keywords'], config['telegram']['chats'], callback, config['telegram']['api_id'],
                              config['telegram']['api_hash'], config['session_name'], config['redis']['host'],
                              config['redis']['port'], config['redis']['password'])

    await crawler.start()


asyncio.run(main())
