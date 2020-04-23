from datetime import datetime
from time import sleep

import pytz
import requests
from bs4 import BeautifulSoup

from providers.base_provider import BaseProvider
from providers.web_base_provider import WebBaseProvider
from templates.single_news import SingleNews
from utils.config import config


class InvestingProvider(WebBaseProvider):

    def __init__(self):
        super().__init__(base_url='https://www.investing.com',
                         news_url='https://www.investing.com/news/latest-news')

    def get_latest_news_with_pc(self, processed_news):
        try:
            page = requests.get(self.NEWS_URL, headers=self.HEADERS)
        except Exception as e:
            print(e)
            return []

        if page.status_code == 500:
            return []

        soup = BeautifulSoup(page.text, "html.parser")

        component = soup.findAll(class_='largeTitle')[0]

        latest_news = component.findAll(class_='textDiv')

        result = []

        for n in latest_news[:5]:

            n_find = n.find()
            if n_find is not None:
                n_href = n_find.get('href')
                if n_href is None:
                    continue
            else:
                continue

            n_title = n_find.get('title')

            if n_title in processed_news.queue:
                continue

            url = self.BASE_URL + n_href

            try:
                news_page = requests.get(url, headers=self.HEADERS)
            except Exception as e:
                try:
                    news_page = requests.get(n_href, headers=self.HEADERS)
                except Exception as e2:
                    print(e2)
                    continue

            n_soup = BeautifulSoup(news_page.text, "html.parser")

            news_datetime = None

            for elem in n_soup.find_all(attrs={'class': 'contentSectionDetails'}):
                try:
                    news_datetime = datetime.strptime(elem.find('span')
                                                      .text.split(')')[0].split('(')[1][:-3], '%b %d, %Y %H:%M%p') \
                        .astimezone(pytz.timezone('EST'))
                    break
                except Exception as e:
                    pass

            text = ''

            if news_datetime is None:
                news_datetime = 'Не удалось получить время новости'
            else:
                for elem in n_soup.find_all(attrs={'class': 'WYSIWYG articlePage'}):
                    text += elem.text

            result.append(SingleNews(n_title, None, url, news_datetime, text,
                                     self.get_symbols_from_text(text)))

        return result

    @staticmethod
    def get_symbols_from_text(text):
        symbols = []
        text = text.replace('(', ' ').replace(')', ' ')

        with open('./filters/files/indexes.txt', 'r') as f:
            for line in f.read().splitlines():
                if ':' + line + ' ' in text:
                    symbols.append(line)

        return symbols

if __name__ == '__main__':
    InvestingProvider().get_latest_news()
