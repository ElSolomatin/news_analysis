from templates.base_news_template import BaseNewsTemplate
from utils.yandex_translate import yandex_translate


class InvestingNews(BaseNewsTemplate):

    def __init__(self, headline, result, url, datetime, text):
        super().__init__(headline, result, url, datetime, text)

        self.translated_headline = yandex_translate.translate(headline)
        self.indices = []

        self.__init_indices()

    def __init_indices(self):
        text = self.text
        text = text.replace('(', ' ').replace(')', ' ')

        with open('./filters/files/indexes.txt', 'r') as f:
            for line in f.read().splitlines():
                if ':' + line + ' ' in text:
                    self.indices.append(line)

    def __str__(self):
        return 'Оригинал: ' + self.headline + '\n' + \
               'Автоматический перевод: ' + self.translated_headline + '\n' + \
               'Предсказание: ' + self.result + '\n' + \
               'Затронутые индексы: ' + str(self.indices) + '\n' + \
               'Время выхода новости: ' + str(self.datetime) + '\n' + \
               'Ссылка на оригинал: ' + self.url + '\n'
