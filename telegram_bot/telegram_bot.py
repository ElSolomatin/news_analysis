import telegram


class TelegramBot:

    def __init__(self):
        TOKEN = "993727911:AAGShCMB0UeY0OZzL5--xkrZgtWy8EfceFA"

        pp = telegram.utils.request.Request(proxy_url='http://51.38.71.101:8080/')
        self.bot = telegram.Bot(token=TOKEN, request=pp)
        res = self.bot.get_me()
        res2= self.bot.get_updates()
        self.chat_id = -1001446599541

    def send(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)
