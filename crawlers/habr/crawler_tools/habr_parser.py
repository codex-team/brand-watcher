import requests
import json
import re
from bs4 import BeautifulSoup
from time import sleep


class HabrParser:
    """This class crawle habr.ru"""
    URL = 'https://habr.com'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Accept': '*/*'
    }

    params = {
        # 'q': brand - from input,
        'target_type': 'posts',
        'order': 'relevance'
    }

    # TODO add redis
    def __init__(self, db, params):
        self.db = db
        self.params = params

    def run_parser(self, num_of_article=10):
        # TODO add logging
        try:
            # in get_article_list we make get request
            article_list = self._get_article_list(num_of_article)
            # parse article link from search page
            articles_dict_data = self._parse_all_articles_into_dict(article_list)
        except requests.Timeout as err_time:
            return f"Ошибка timeout, args {err_time.args}, error: ', err_time"
        except requests.HTTPError as err:
            code = err.response.status_code
            return f"Ошибка args: {0}, code: {1}".format(err.args, code)
        except requests.RequestException as err:
            return f'Error!\n {err.args}'
        except AttributeError as err:
            return f'Some tag or class was changed: \n{err}'

        json_data = self._dict_to_json(articles_dict_data)

        return json_data

    def _parse_single_article(self, url: str) -> dict:
        req = requests.get(url)
        src = req.text

        soup = BeautifulSoup(src, 'lxml')

        title = soup.find('h1').text

        meta_data = soup.find('div', class_='tm-article-snippet__meta')
        author = meta_data.find('span', class_='tm-user-info__user').text.strip()
        data_published = meta_data.find('time')['datetime']

        article_text = soup.find('div', id='post-content-body').text
        text = re.sub('\n', ' ', article_text)

        result_dict = {
            'title': title,
            'URL': url,
            'author': author,
            'data_published': data_published,
            'text': text,
        }

        return result_dict

    def _get_article_list(self, num_of_article: int) -> list:
        article_list = list()
        page = 1

        # TODO if num > 10000, paginator link active
        # TODO add "ALL" num and default article num
        while num_of_article > 0:
            req = requests.get(self.URL + f'/search/page{page}', params=self.params, headers=self.HEADERS)
            src = req.text

            soup = BeautifulSoup(src, 'lxml')

            empty_page = soup.find('div', class_='tm-empty-placeholder')
            if empty_page:
                return []
            # https://habr.com/ru/search/page1/?target_type=posts&order=relevance&q=python
            all_article = soup.find('div', class_='tm-articles-list')
            if num_of_article <= 20:
                article_list += all_article.find_all('article', class_='tm-articles-list__item')[:num_of_article:]
                num_of_article = 0
            else:
                article_list += all_article.find_all('article', class_='tm-articles-list__item')
                page += 1
                num_of_article -= 20

        return article_list

    def _parse_all_articles_into_dict(self, articles: list) -> dict:
        result_dict = {}

        for i, article in enumerate(articles):
            article_url = article.find('a', class_='tm-article-snippet__title-link')['href']
            article_url = self.URL + article_url

            # Search data in redis
            data_redis = self.db.find_data(article_url)

            if data_redis:
                print(f'Data is founded in DB: {article_url}')
            elif 'post' in article_url:
                print(f'Article #{i+1}', article_url)

                # make get request and parse data from article
                article_data = self._parse_single_article(article_url)
                result_dict[i] = article_data

                # Save in redis
                string_result = json.dumps(result_dict)
                self.db.save_data(article_url, string_result)
            else:
                print(f'Article #{i+1} is not post, its url: {article_url}')

        return result_dict

    def _dict_to_json(self, dict):
        return json.dumps(dict, indent=4, ensure_ascii=False)

    def sleep(self, time):
        sleep(time)


