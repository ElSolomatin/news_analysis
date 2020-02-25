import logging
import queue

from time import sleep

from filters.simple_filter import SimpleFilter
from postprocessors.simple_postprocessor import SimplePostprocessor
from predictors.cnn.cnn_predictor import CNNPredictor
from providers.finnhub_provider import FinnhubProvider
from providers.investing_provider import InvestingProvider
from providers.the_guardian_provider import TheGuardianProvider
from telegram_bot.telegram_bot import TelegramBot
from utils.config import config


class Analysis:

    __slots__ = [
        'processed_news',
        'telegram_bot',
        'provider',
        'filter',
        'config',
        'predictor',
        'postprocessor',
        'logger'
    ]

    def __init__(self):
        self.processed_news = queue.Queue(config['queue_size'])

        self.provider = InvestingProvider()

        self.telegram_bot = TelegramBot(config['telegram_bot_token'])

        self.filter = SimpleFilter()

        self.predictor = CNNPredictor(config['cnn_models_path'])

        self.postprocessor = SimplePostprocessor()

        self.logger = logging.getLogger('Analysis')
        self.logger.setLevel(logging.DEBUG)

    def start(self):
        self.logger.info('Analysis started')

        while True:

            latest_news = self.provider.get_latest_news_with_pc(self.processed_news)

            for news in latest_news:

                if news.headline in self.processed_news.queue:
                    continue

                self.processed_news.put(news.headline)

                # if self.filter.is_valid(news):

                result = self.predictor.predict(news.headline)

                notifications = self.postprocessor.run(news, result)

                news.result = result

                try:
                    self.telegram_bot.send(str(news))
                except Exception as e:
                    self.logger.error(e)

                if notifications is not None:
                    for notification in notifications:
                        self.telegram_bot.send(notification)

            sleep(5)


if __name__ == '__main__':
    Analysis().start()
