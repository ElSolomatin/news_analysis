import requests

from providers.base_provider import BaseProvider
from templates.base_news_template import BaseNewsTemplate


class FinnhubProvider(BaseProvider):

    def __init__(self):
        super().__init__()

        self.token = "bp62g6frh5rcobn2dpqg"

    def get_latest_news(self):
        return [BaseNewsTemplate(news['headline'], None, news['url'], news['datetime'])
                for news in requests.get(
                'https://finnhub.io/api/v1/news?category=general&token=bp62g6frh5rcobn2dpqg').json()]
