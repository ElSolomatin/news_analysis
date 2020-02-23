from datetime import datetime


class BaseNewsTemplate:
    def __init__(self, headline, result, url, datetime_str):
        self.headline = headline
        self.url = url
        self.result = result
        self.datetime = datetime_str

    def get_str(self):
        return self.headline + '\n' + self.result + '\n' + self.datetime + '\n' + self.url
