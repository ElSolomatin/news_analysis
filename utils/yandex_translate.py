from yandex.Translater import Translater

from utils.config import config


class YandexTranslate:

    def __init__(self, key):
        self.key = key
        self.__translator = Translater(key, from_lang='en', to_lang='ru')

    def translate(self, text):
        self.__translator.set_text(text)
        return self.__translator.translate()


yandex_translate = YandexTranslate(config['api_keys']['yandex_translate'])
