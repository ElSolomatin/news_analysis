from templates.base_news_template import BaseNewsTemplate
from utils.yandex_translate import yandex_translate


class SingleNews(BaseNewsTemplate):

    def __init__(self, headline, ai_predict, url, datetime, text, symbols):
        super().__init__(headline, ai_predict, url, datetime, text, symbols=symbols)

        self.translated_headline = yandex_translate.translate(headline)

    def __str__(self):
        return 'Оригинал: ' + self.headline + '\n' + \
               'Автоматический перевод: ' + self.translated_headline + '\n' + \
               'Затронутые акции: ' + str(self.symbols) + '\n' + \
               'Время новости: ' + str(self.datetime) + '\n' + \
               'Ссылка на оригинал: ' + self.url + '\n'
