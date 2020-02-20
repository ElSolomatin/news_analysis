import logging
import queue
import json

from time import sleep

from filters.simple_filter import SimpleFilter
from postprocessors.simple_postprocessor import SimplePostprocessor
from predictors.cnn.cnn_predictor import CNNPredictor
from providers.finnhub_provider import FinnhubProvider
from telegram_bot.telegram_bot import TelegramBot


class Analysis:

    __slots__ = [
        'processed_news',
        'telegram_bot',
        'provider',
        'filter',
        'config',
        'predictor',
        'postprocessor'
    ]

    def __init__(self):
        # Init config
        with open('config.json') as config_file:
            self.config = json.load(config_file)

        self.processed_news = queue.Queue(self.config['queue_size'])

        self.provider = FinnhubProvider()

        self.telegram_bot = TelegramBot()

        self.filter = SimpleFilter()

        self.predictor = CNNPredictor(self.config['cnn_models_path'])

        self.postprocessor = SimplePostprocessor()

    def start(self):

        logging.info('Analysis started')

        while True:

            latest_news = self.provider.get_latest_news()

            for news in latest_news:

                if news.headline in self.processed_news.queue:
                    continue

                self.processed_news.put(news.headline)

                if self.filter.is_valid(news):

                    result = self.predictor.predict(news.headline)

                    notifications = self.postprocessor.run(news, result)

                    if result is not None:
                        news.result = result

                        self.telegram_bot.send(news.get_str())

                    if notifications is not None:
                        for notification in notifications:
                            self.telegram_bot.send(notification)

            sleep(5)


if __name__ == '__main__':
    Analysis().start()
