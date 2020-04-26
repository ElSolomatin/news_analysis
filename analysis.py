import logging
import queue

from time import sleep

from filters.simple_filter import SimpleFilter
from postprocessors.simple_postprocessor import SimplePostprocessor
from predictors.cnn.cnn_predictor import CNNPredictor
from providers.finnhub_provider import FinnhubProvider
from providers.investing_provider import InvestingProvider
from providers.marketwatch_provider import MarketWatchProvider
from providers.the_guardian_provider import TheGuardianProvider
from telegram_bot.telegram_bot import TelegramBot
from utils.config import config


class Analysis:

    __slots__ = [
        'processed_news',
        'telegram_bot',
        'news_providers',
        'filter',
        'config',
        'predictor',
        'postprocessor',
        'logger'
    ]

    def __init__(self):
        self.processed_news = queue.Queue(config['queue_size'])

        self.news_providers = [
            # InvestingProvider(),
            MarketWatchProvider()
        ]

        self.telegram_bot = TelegramBot(config['telegram_bot_token'])

        self.filter = SimpleFilter()

        # self.predictor = CNNPredictor(config['cnn_models_path'])

        self.postprocessor = SimplePostprocessor()

        self.logger = logging.getLogger('Analysis')
        self.logger.setLevel(logging.DEBUG)

        try:
            self.idle_start()
        except Exception as e:
            print('idle', e)

    def idle_start(self):
        self.logger.info('Idle started')
        for provider in self.news_providers:
            self.logger.info('Idle still working...')
            latest_news = provider.get_latest_news_with_pc(self.processed_news)

            for news in latest_news:
                self.processed_news.put(news.headline)
        self.logger.info('Idle done')

    def start(self):
        self.logger.info('Analysis started')

        while True:
            try:
                for provider in self.news_providers:
                    latest_news = provider.get_latest_news_with_pc(self.processed_news)

                    for news in latest_news:

                        if news.headline in self.processed_news.queue:
                            continue

                        self.processed_news.put(news.headline)

                        # if self.filter.is_valid(news):

                        # result = self.predictor.predict(news.headline)
                        #
                        # notifications = self.postprocessor.run(news, result)

                        news.result = None

                        try:
                            print('start sending...')
                            self.telegram_bot.send(str(news))
                            print(str(news))
                        except Exception as e:
                            self.logger.error(e)
                            print(1)
                            self.telegram_bot = TelegramBot(config['telegram_bot_token'])

                        # if notifications is not None:
                        #     for notification in notifications:
                        #         self.telegram_bot.send(notification)
            except Exception as e:
                print('main loop fail', e)


if __name__ == '__main__':
    Analysis().start()
