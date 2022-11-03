import logging
import os

import telegram


class TgbotLogger(logging.Handler):
    
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def create_logger_bot():
    bot = telegram.Bot(token=str(os.getenv("TG_LOGGER_TOKEN")))
    logger = logging.getLogger("botlog")
    logger.setLevel(logging.WARNING)
    bot_logger = TgbotLogger(bot, os.getenv("TG_CHAT_ID"))
    logger.addHandler(bot_logger)

