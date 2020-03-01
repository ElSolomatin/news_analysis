import time

import requests

from telegram_bot.telegram_bot import TelegramBot
from utils.config import config


class PriceChecker:

    def __init__(self):
        self.telegram_bot = TelegramBot(config['telegram_bot_token'])
        self.indices = {'SPX': 0,
                        'N225': 0,
                        'DAX': 0,
                        'FTSE': 0,
                        'FRANCE40': 0,
                        'AMD': 0,
                        'TSLA': 0,
                        'USDRUR': 0,
                        'EURRUR': 0
                        }

        self.threshold = 0.05

    def run(self):
        while True:
            for idx in self.indices:

                if len(idx) != 6:
                    index = '%23' + idx
                else:
                    index = idx

                res = requests.get('https://quotes.instaforex.com/api/quotesTick?q=' + index).json()[0]

                if self.indices[idx] == 0:
                    self.indices[idx] = res['ask']
                    continue

                diff = self.indices[idx] - res['ask']

                change = 100 * diff / self.indices[idx]

                if abs(change) > self.threshold:
                    self.telegram_bot.send(idx + ' Изменения в цене на ' + str(change) + '%')

                time.sleep(2)


if __name__ == '__main__':
    PriceChecker().run()
