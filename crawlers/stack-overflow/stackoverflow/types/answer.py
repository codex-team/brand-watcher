import requests
from typing import TypeVar, Type
import logging

API_URL = "https://api.stackexchange.com/2.3/questions/"

# Filter to add more parameters to answers response
FILTER = "!*MZqiH2sG_JWt3xD"

T = TypeVar('T', bound='Answer')


class Answer:
    """
    The Answer has methods to work with stackOverflow answers
    :param answer_id - id of answer
    :param title - answer title
    :param body: answer body
    :param url - answer link
    :param score - answer score
    :param date - answer creation date
    """

    def __init__(self, answer_id, title: str, body: str, url: str, score: int, date):
        self.answer_id = answer_id
        self.title = title
        self.body = body
        self.url = url
        self.score = score
        self.date = date

    @classmethod
    def find_by_question_id(cls: Type[T], question_id: int) -> list[T]:
        """
        Find answers by question id
        :param question_id: question id
        :returns: list of answers
        """

        answers = []

        # Make data for request
        data = {
            "site": "stackoverflow",
            "filter": FILTER
        }

        res = requests.get(f"{API_URL}{question_id}/answers", params=data)

        try:
            for item in res.json()['items']:
                answer = cls(item['answer_id'], item['title'], item['body'], item['link'], item['score'],
                             item['creation_date'])

                answers.append(answer)
        except Exception as e:
            logging.warning(f'Invalid response structure: {e}')
        return answers




