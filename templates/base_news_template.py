from datetime import datetime


class BaseNewsTemplate:
    def __init__(self, headline, result, url, dt, text=''):
        self.headline = headline
        self.url = url

        if result is None:
            self.result = 'Неизвестно'
        else:
            self.result = result

        self.datetime = dt
        self.text = text

    def __str__(self):
        return self.headline + '\n' + self.result + '\n' + self.datetime + '\n' + self.url
