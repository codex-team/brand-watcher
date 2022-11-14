import json

from stackoverflow.types.question import Question
from stackoverflow.db.db import Db
from stackoverflow.utils.utils import Utils
from stackoverflow.broker.broker import Broker


class StackOverflowCrawler:
    """
    The StackOverflowCrawler make crawling of stackOverflow
    :param keywords - keywords to find
    :param db - database instance
    """

    def __init__(self, keywords: list[str], db: Db, broker: Broker):
        self.keywords = keywords
        self.db = db
        self.broker = broker

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

            if not res:
                # Convert dict data to string
                data = json.dumps(question.to_dict())

                self.broker.send(data)

                self.db.save_data(hashed_question_url, data)




