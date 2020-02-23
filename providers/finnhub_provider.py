from datetime import datetime

import requests

from providers.base_provider import BaseProvider
from templates.base_news_template import BaseNewsTemplate


class FinnhubProvider(BaseProvider):

    def __init__(self, api_key):
        super().__init__()

        self.api_key = api_key

    def get_latest_news(self):
        return [BaseNewsTemplate(news['headline'],
                                 None, news['url'],
                                 datetime.fromtimestamp(news['datetime']))
                for news in requests.get(
                'https://finnhub.io/api/v1/news?category=general&token=' + self.api_key).json()]
