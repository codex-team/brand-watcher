import json

from youtube.utils.functions import Functions
from youtube.db.db import Db
from youtube.utils.utils import Utils
from googleapiclient.discovery import build


class YouTubeCrawler:
    """
    The YouTubeCrawler make crawling of YouTube
    :param keywords - keywords to find
    :param db - database instance
    :param api_key - 
    """

    def __init__(self, keywords: list[str], db: Db, api_key):
        self.keywords = keywords
        self.db = db
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def crawl(self):
        """
        Crawling service
        """
        videos = []

        # Find questions with keywords
        for keyword in self.keywords:
            videos += Functions.search_video(keyword, self.youtube)

        # Check of founded videos, if it exists in database
        for video in videos:
            hashed_video_url = Utils.hash_data(video['url'])
            res = self.db.find_data(hashed_video_url)

            print(f"Founded data: {res}")

            if not res:
                # Convert dict data to string
                data = json.dumps(video)

                self.db.save_data(hashed_video_url, data)

                print(f"New data: {data}")



