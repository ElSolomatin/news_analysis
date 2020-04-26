from datetime import datetime
from queue import Queue
from time import sleep

import pytz
import requests
from bs4 import BeautifulSoup

from providers.base_provider import BaseProvider
# from utils.config import config
from providers.web_base_provider import WebBaseProvider
from templates.single_news import SingleNews


class MarketWatchProvider(WebBaseProvider):

    def __init__(self):

        super().__init__(base_url='https://www.marketwatch.com/',
                         news_url='https://www.marketwatch.com/latest-news')

    def get_latest_news_with_pc(self, processed_news):
        try:
            page = requests.get(self.NEWS_URL, headers=self.HEADERS)
        except Exception as e:
            print(e)
            return []

        if page.status_code == 500:
            return []

        soup = BeautifulSoup(page.text, "html.parser")

        target_component = soup.findAll(class_='component component--module more-headlines')[0]
        latest_news = target_component.findAll(class_='article__content')
        result = []

        for news in latest_news[:5]:

            headline = news.findAll(class_='article__headline')[0].find()

            if headline is None or headline.text == '' or headline.text in processed_news.queue:
                continue

            details = news.findAll(class_='article__details')[0].find()

            try:
                news_page = requests.get(headline['href'], headers=self.HEADERS)
            except Exception as e:
                print(e)
                print(headline['href'])
                continue

            news_soup = BeautifulSoup(
                news_page.text,
                "html.parser"
            )

            referenced_symbols = []
            raw_stocks = news_soup.findAll('span', class_='symbol')

            for stock in raw_stocks:
                referenced_symbols.append(stock.text)

            result.append(SingleNews(headline.text, ai_predict=None, url=headline['href'], datetime=details['data-est'],
                                     symbols=referenced_symbols, text=''))
        return result


if __name__ == '__main__':
    res = MarketWatchProvider().get_latest_news_with_pc(Queue())
    print(res)