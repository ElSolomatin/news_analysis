import telegram


class TelegramBot:

    def __init__(self, token):
        self.bot = telegram.Bot(token=token)
        self.chat_id = -1001446599541

    def send(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)
