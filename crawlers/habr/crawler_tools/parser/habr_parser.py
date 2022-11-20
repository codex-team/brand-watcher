import logging

from crawlers.habr.crawler_tools.utils.utils import dict_to_json
from crawlers.habr.crawler_tools.parser.base_parser import BaseParser


# TODO One exception on single page fail all parsing: add saving every article
# TODO Write user exception for controlling Attribute error or NoBrandError.
# TODO Add delay between request

class HabrParser(BaseParser):
    """This class crawlers habr.ru"""

    URL = 'https://habr.com'

    def run_parser(self, required_page_number):
        """
        Main function that start parsing
        Realized @required_page_number@ feature for amount controlling. Every page contains 20 articles
        """
        try:
            article_list = self._get_article_url_list(required_page_number)
            articles_dict_data = self._iterate_by_article_url_list(article_list)
        except AttributeError as err:
            logging.warning(f'Some tag or class was changed on habr.com, {err}')
            return None

        data = dict_to_json(articles_dict_data)

        return data

    def _get_article_url_list(self, required_page_number) -> list or None:
        """
        It searches brand with the help of search form
        and collect links to necessary articles
        :returns links of required articles
        """
        articles_urls_list = list()

        soup = self.get_soup(self.URL + '/ru/search/', self.params)
        empty_page = soup.find('div', class_='tm-empty-placeholder')

        if empty_page:
            logging.warning(f'No one articles from habr.com with brand "{self.params["q"]}"')
            return None

        page_number = 1
        error = None
        while error is None and page_number != required_page_number + 1:
            all_article = soup.find('div', class_='tm-articles-list')
            articles_urls_list += all_article.find_all('article', class_='tm-articles-list__item')

            page_number += 1
            soup = self.get_soup(self.URL + f'/search/page{page_number}', self.params)
            error = soup.find('div', class_='tm-error-message')

        return articles_urls_list

    def _iterate_by_article_url_list(self, articles: list) -> dict:
        """
        Find urls from articles list and
        make requests to single article to collect information
        """
        result_dict = {}

        for order_number, article in enumerate(articles, start=1):
            article_url = article.find('a', class_='tm-article-snippet__title-link')['href']
            article_url = self.URL + article_url

            # Search data in redis
            data_redis = self.db.find_data(article_url)

            if data_redis:
                logging.info(f'Data is founded in DB: {article_url}')
                continue

            result_dict[order_number] = self.parse_single_article(order_number, article_url)

        return result_dict

    def parse_single_article(self, order_number, article_url):
        """Parse single article using url"""
        post_article_data = self.post_handler(
            article_url,
            h1_class='tm-article-snippet__title tm-article-snippet__title_h1',
            meta_data_class='tm-article-snippet__meta',
            author_class='tm-user-info__user',
            content_id='post-content-body'
        )
        logging.info(f'Article #{order_number}, {article_url}')
        self.save_in_db(article_url, post_article_data)

        return post_article_data



