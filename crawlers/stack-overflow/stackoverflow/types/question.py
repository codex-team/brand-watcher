import logging
import requests
from typing import TypeVar, Type

from stackoverflow.types.answer import Answer

API_URL = 'https://api.stackexchange.com/2.3/search'

T = TypeVar('T', bound='Question')

FILTER = '!nOedRLezYU'


class Question:
    """
    The Question make methods to work with stackOverflow questions
    :param question_id - id of question
    :param title - question title
    :param url - question link
    :param date - question creation date
    :param author - question author name
    :param keyword - founded keyword
    :param body - question body
    """

    def __init__(self, question_id, title: str, url: str, date, author: str, keyword: str, body: str):
        self.question_id = question_id
        self.title = title
        self.url = url
        self.date = date
        self.author = author
        self.answers: list[Answer] = []
        self.keyword = keyword
        self.body = body

    @classmethod
    def find_by_tag(cls: Type[T], tag: str) -> list[T]:
        """
        Find questions by tag
        :param tag: tag to find
        :returns: list of questions
        """

        questions = []

        # Create data for api request
        params = {
            "order": "desc",
            "sort": "activity",
            "site": "stackoverflow",
            "tagged": tag,
            "filter": FILTER,
        }

        res = requests.get(API_URL, params=params)
        try:
            # Check founded data
            for item in res.json()['items']:
                question = cls(item['question_id'], item['title'], item['link'], item['creation_date'],
                               item['owner']['display_name'], tag, item['body'])

                questions.append(question)
        except Exception as e:
            logging.warning(f'Invalid response structure: {e}')

        return questions

    def to_dict(self):
        """
        Convert question to dict
        :returns: question converted to dict
        """

        answers = []

        # Convert to dict the list of answers
        for answer in self.answers:
            answers.append(answer.title)

        return {
            "title": self.title,
            "url": self.url,
            "date": self.date,
            "author": self.author,
            "body": self.body,
            "comments": answers,
            "keyword": self.keyword,
            "source": 'stack-overflow'
        }


