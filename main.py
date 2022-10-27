import os
import time

from dotenv import load_dotenv
import requests
import telegram

from loguru import logger


URL = "https://dvmn.org/api/long_polling/"


if __name__ == "__main__":
    load_dotenv()
    autorization_header = {
        "Authorization": f"Token {os.getenv('DVMN_TOKEN')}"
    }
    params = {
        "timestamp": "" 
    }
    bot = telegram.Bot(token=str(os.getenv("TG_TOKEN")))
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
            logger.info(timestamp)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(60)
