from datetime import datetime
from time import sleep

import pytz
import requests
from bs4 import BeautifulSoup

from providers.base_provider import BaseProvider
from templates.investing_news import InvestingNews
from utils.config import config


class InvestingProvider(BaseProvider):
    url = 'https://www.investing.com/news/stock-market-news'

    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.investing.com'
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def get_latest_news_with_pc(self, processed_news):
        page = requests.get('https://www.investing.com/news/stock-market-news', headers=self.headers)

        soup = BeautifulSoup(page.text, "html.parser")
        latest_news = soup.findAll(class_='textDiv')

        result = []

        i = 0

        for n in latest_news:

            n_find = n.find()
            if n_find is not None:
                n_href = n_find.get('href')
                if n_href is None:
                    continue
            else:
                continue

            n_title = n_find.get('title')

            if n_title in processed_news.queue or i > config['news_limit']:
                continue

            i += 1

            url = self.base_url + n_href

            news_page = requests.get(url, headers=self.headers)

            n_soup = BeautifulSoup(news_page.text, "html.parser")

            for elem in n_soup.find_all(attrs={'class': 'contentSectionDetails'}):
                try:
                    news_datetime = datetime.strptime(elem.find('span')
                                                      .text.split(')')[0].split('(')[1][:-3], '%b %d, %Y %H:%M%p') \
                        .astimezone(pytz.timezone('EST'))
                    break
                except Exception as e:
                    pass

            text = ''
            for elem in n_soup.find_all(attrs={'class': 'WYSIWYG articlePage'}):
                text += elem.text

            result.append(InvestingNews(n_title, None, url, news_datetime, text))

            sleep(2)

        return result


if __name__ == '__main__':
    InvestingProvider().get_latest_news()
