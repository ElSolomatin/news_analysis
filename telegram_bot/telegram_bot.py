import telegram


class TelegramBot:

    def __init__(self, token):
        self.bot = telegram.Bot(token=token)
        # self.bot.get_updates
        self.chat_id = -355731380

    def send(self, message):

        # chat_ids = []

        self.bot.send_message(chat_id=self.chat_id, text=message)

        # for update in self.bot.get_updates():
        #     if update.effective_chat.id not in chat_ids:
        #         chat_ids.append(update.effective_chat.id)
        #
        # for id in chat_ids:
        #     self.bot.send_message(chat_id=id, text=message)
