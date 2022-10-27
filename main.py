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
    try: 
        while True:
            response = requests.get(
                URL, autorization_header, params
            )
            response.raise_for_status()
            check_lesson_params = response.json()
            timestamp = check_lesson_params.get("timestamp_to_request")
            status = check_lesson_params.get("status")
            if status == "found":
                remark = check_lesson_params["new_attempts"][0]["is_negative"]
                lesson_url = check_lesson_params["new_attempts"][0]["lesson_url"]
                lesson = check_lesson_params["new_attempts"][0]["lesson_title"]
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
            logger.info(timestamp)
            params = {
                "timestamp": timestamp
            }
    except requests.exceptions.ReadTimeout:
        time.sleep(20)
    except requests.exceptions.ConnectionError:
        time.sleep(60)
