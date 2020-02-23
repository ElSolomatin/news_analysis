import requests

from providers.base_provider import BaseProvider
from templates.base_news_template import BaseNewsTemplate


class TheGuardianProvider(BaseProvider):

    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def get_latest_news(self):
        url = "http://content.guardianapis.com/business/stock-markets"

        payload = {}
        headers = {
            'api-key': self.api_key
        }

        response = requests.request("GET", url,
                                    headers=headers,
                                    data=payload).json()['response']
        return [BaseNewsTemplate(
            news['webTitle'],
            None,
            news['webUrl'],
            news['webPublicationDate'])
            for news in response['results']]
