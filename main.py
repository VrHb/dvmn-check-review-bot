import os
import time
import logging

from dotenv import load_dotenv
import requests
import telegram


logger = logging.getLogger("botlog")

URL = "https://dvmn.org/api/long_polling/"

class TgbotLogger(logging.Handler):
    
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)

def main():
    load_dotenv()
    autorization_header = {
        "Authorization": f"Token {os.getenv('DVMN_TOKEN')}"
    }
    params = {
        "timestamp": "" 
    }
    bot = telegram.Bot(token=str(os.getenv("TG_TOKEN")))
    logger_bot = telegram.Bot(token=str(os.getenv("TG_LOGGER_TOKEN")))
    logger.setLevel(logging.WARNING)
    bot_logger = TgbotLogger(logger_bot, os.getenv("TG_CHAT_ID"))
    logger.addHandler(bot_logger)
    logging.basicConfig(format="%(asctime)s %(lineno)d %(message)s")
    logger.warning("Бот запущен!")
    while True:
        try:
            response = requests.get(
                URL, headers=autorization_header, params=params, timeout=10
            )
            response.raise_for_status()
            check_lesson_params = response.json()
            timestamp = check_lesson_params.get("timestamp_to_request")
            status = check_lesson_params.get("status")
            if status == "found":
                timestamp = check_lesson_params["last_attempt_timestamp"]
                attempts = check_lesson_params["new_attempts"][0]
                remark = attempts["is_negative"]
                lesson_url = attempts["lesson_url"]
                lesson = attempts["lesson_title"]
                if remark:
                    bot.send_message(
                        text=f"Преподаватель проверил работу *{lesson}* {lesson_url}\n\n К сожалению, в работе нашлись ошибки!",
                        chat_id=os.getenv("TG_CHAT_ID"),
                        parse_mode="Markdown"
                        )
                else:
                    bot.send_message(
                        text=f"Преподаватель проверил работу *{lesson}* {lesson_url}\n\n Преподавателю все понравилось, можно приступать к следующему уроку!",
                        chat_id=os.getenv("TG_CHAT_ID"),
                        parse_mode="Markdown"
                        )
            params = {
                "timestamp": timestamp
            }
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Бот упал с ошибкой:\n{e}")
            time.sleep(60)


if __name__ == "__main__":
   main()
