from datetime import datetime


class BaseNewsTemplate:
    def __init__(self, headline, ai_predict, url, dt, text='', symbols=None):

        if symbols is None:
            symbols = []

        self.headline = headline

        self.url = url

        self.symbols = symbols

        if ai_predict is None:
            self.ai_predict = 'Неизвестно'
        else:
            self.ai_predict = ai_predict

        self.datetime = dt
        self.text = text

    def __str__(self):
        return self.headline + '\n' + self.ai_predict + '\n' + self.datetime + '\n' + self.url
