import json
import logging
from telethon import events
from telethon import TelegramClient

from crawler.types.group import Group
from crawler.types.message import Message
from crawler.db.db import Db
from crawler.utils.utils import Utils

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class TelegramCrawler:
    """
    The TelegramCrawler gets data from telegram
    :param keywords - words to find
    :param telegram_public - telegram public channels or chats
    :param callback - function to handle found information
    :param api_id - id of telegram app
    :param api_hash - hash of telegram app
    """

    def __init__(self, keywords, telegram_public, callback, api_id, api_hash, session_name,
                 redis_host, redis_port, redis_password):
        self.database = Db(redis_host, redis_port, redis_password)
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = None
        self.callback = callback
        self.channels = []
        self.keywords = keywords
        self.telegram_public = telegram_public

    async def start(self):
        """
        Initiating Telegram Client and starting crawling
        """
        async with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            self.client = client
            await self.__prepare_crawling()
            await self.__start_crawling()

    async def __prepare_crawling(self):
        """
        Create new instances of Group, joining to telegram channels
        """
        for channel in self.telegram_public:
            channel = await Group.get_group_by_data(channel, self.client)
            await channel.join_to_group()
            self.channels.append(channel)

    async def __start_crawling(self):
        """
        Make first search in public channels and chats
        """
        # Take a look in the list of saved channels
        for channel in self.channels:
            messages = await channel.search_messages(self.keywords)

            # Parse found messages
            for message in messages:
                msg = Message(message)
                await msg.get_replies(self.client)
                await self.__parse_message(msg)

        # Create handler for incoming messages
        @self.client.on(events.NewMessage)
        async def handler(event):
            """
            Get message from incoming event, and check it
            :param event: incoming telegram event
            """
            try:
                message_from_event = Message(event.original_update.message)
                if message_from_event.search_by_keywords(self.keywords):
                    await self.__parse_message(message_from_event)
            except (Exception,):
                print('Invalid type of message')

        # Run telegram client to wait for incoming events
        await self.client.run_until_disconnected()

    async def __parse_message(self, message: Message):
        """
        Create object for callback function and call it
        :param message: message to parse
        """
        channel = await Group.get_group_by_data(message.group_id, self.client)

        # Create hash
        event_id = Utils.hash_data(str(message.message_id) + str(channel.group_id))

        # Check if data already exists in database
        res = self.database.find_data(event_id)

        if res:
            return

        comments = []

        for comment in message.comments:
            comments.append(comment.to_dict())

        data = {
            'text': message.text,
            'date': message.date,
            'author': channel.title,
            'comments': comments
        }

        str_data = json.dumps(data)

        # Save new data to database
        self.database.save_data(event_id, str_data)

        await self.callback(data)
