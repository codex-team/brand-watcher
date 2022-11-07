import json

from stackoverflow.types.question import Question
from stackoverflow.db.db import Db
from stackoverflow.utils.utils import Utils


class StackOverflowCrawler:
    """
    The StackOverflowCrawler make crawling of stackOverflow
    :param keywords - keywords to find
    :param redis_host - host for redis database
    :param redis_port- port for redis database
    :param redis_password - password for redis database
    """

    def __init__(self, keywords: list[str], redis_host: str, redis_port: int, redis_password: str = ''):
        self.keywords = keywords
        self.db = Db(redis_host, redis_port, redis_password)

    def crawl(self):
        """
        Crawling service
        """
        questions = []

        # Find questions with keywords
        for keyword in self.keywords:
            questions += Question.find_by_tag(keyword)

        # Check of founded questions, if it exists in database
        for question in questions:
            hashed_question_url = Utils.hash_data(question.url)
            res = self.db.find_data(hashed_question_url)

            print(f"Founded data: {res}")

            if not res:
                # Convert dict data to string
                data = json.dumps(question.to_dict())

                self.db.save_data(hashed_question_url, data)

                print(f"New data: {data}")



