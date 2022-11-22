import logging

from crawler_tools.utils.utils import dict_to_json
from crawler_tools.parser.base_parser import BaseParser


class HabrParser(BaseParser):
    """This class crawlers habr.ru"""

    URL = 'https://habr.com'

    PARAMS = {
        "target_type": "posts",
        "order": "relevance",
        "q": ""
    }

    HABR_ClASSES = {
        'h1_class': 'tm-article-snippet__title tm-article-snippet__title_h1',
        'meta_data_class': 'tm-article-snippet__meta',
        'author_class': 'tm-user-info__user',
        'content_id': 'post-content-body',
        'absence': ['tm-expired-company']
    }

    def run_parser(self, required_page_number):
        """
        Main function that start parsing
        Realized @required_page_number@ feature for amount controlling. Every page contains 20 articles
        """
        result_dict = {}

        article_list = self._get_article_url_list(required_page_number)
        for order_number, article_url in enumerate(article_list, start=1):
            try:
                single_article_data = self.parse_single_article(order_number, article_url)
                if single_article_data:
                    result_dict[order_number] = single_article_data
            except AttributeError as err:
                logging.warning(f'Article {self.URL + article_url} is not parsed. '
                                f'Probably some tag or class was changed, {err}')
                continue

        data = dict_to_json(result_dict)

        return data

    def _get_article_url_list(self, required_page_number) -> list or None:
        """
        It searches brand with the help of search form
        and collect links to necessary articles
        :returns links of required articles
        """
        articles_short_list = list()

        soup = self.get_soup(self.URL + '/ru/search/', self.PARAMS)

        empty_page = soup.find('div', class_='tm-empty-placeholder')
        if empty_page:
            logging.warning(f'No one articles from habr.com with brand "{self.PARAMS["q"]}"')
            return []

        page_number = 1
        error = None
        while error is None and page_number != required_page_number + 1:
            all_article = soup.find('div', class_='tm-articles-list')
            articles_short_list += all_article.find_all('article', class_='tm-articles-list__item')
            page_number += 1
            soup = self.get_soup(self.URL + f'/search/page{page_number}', self.PARAMS)
            error = soup.find('div', class_='tm-error-message')

        articles_urls_list = [
            article.find('a', class_='tm-article-snippet__title-link')['href'] for article in articles_short_list
        ]

        # Filtering url if it is in Redis
        urls_list_without_repetition = [url for url in articles_urls_list
                                        if self.db.find_data(url, keyword=self.keyword) is None]

        return urls_list_without_repetition

    def parse_single_article(self, order_number, article_url):
        """Parse single article using url"""
        single_article_data = self.post_handler(self.URL + article_url, **self.HABR_ClASSES)
        logging.info(f'Article #{order_number}, {article_url}')
        self.db.save_data(article_url, self.keyword, single_article_data['data_published'])

        return single_article_data
