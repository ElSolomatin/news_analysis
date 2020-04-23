from providers.base_provider import BaseProvider


class WebBaseProvider(BaseProvider):

    def __init__(self, base_url, news_url):
        super().__init__()
        self.BASE_URL = base_url
        self.NEWS_URL = news_url

        self.HEADERS = {'User-Agent': 'Mozilla/5.0'}
