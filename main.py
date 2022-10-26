import os
import time

from dotenv import load_dotenv
import requests
import telegram

from loguru import logger


url_list = "https://dvmn.org/api/user_reviews/"
url_longpolling = "https://dvmn.org/api/long_polling/"


def get_devman_userrewiews_info(url, token, *args):
    response = requests.get(url, headers=token)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    load_dotenv()
    autorization_header = {
        "Authorization": f"Token {os.getenv('DVMN_TOKEN')}"
    }
    params = {
        "timestamp": "" 
    }
    bot = telegram.Bot(token=str(os.getenv("TG_TOKEN")))
    updates = bot.get_updates()
    try: 
        while True:
            polling_response = get_devman_userrewiews_info(
                url_longpolling, autorization_header, params
            )
            logger.info(polling_response)
            timestamp = polling_response.get("timestamp_to_request")
            status = polling_response.get("status")
            if status == "found":
                remark = polling_response["new_attempts"][0]["is_negative"]
                lesson_url = polling_response["new_attempts"][0]["lesson_url"]
                lesson = polling_response["new_attempts"][0]["lesson_title"]
                if remark:
                    bot.send_message(
                        text=f"Преподаватель проверил работу *{lesson}* {lesson_url}\n\n К сожалению, в работе нашлись ошибки!",
                        chat_id=os.getenv("CHAT_ID"),
                        parse_mode="MArkdown"
                        )
                else:
                    bot.send_message(
                        text=f"Преподаватель проверил работу *{lesson}* {lesson_url}\n\n Преподавателю все понравилось, можно приступать к следующему уроку!",
                        chat_id=os.getenv("CHAT_ID"),
                        parse_mode="Markdown"
                        )
            logger.info(timestamp)
            logger.info(updates[0].message.from_user.id)
            params = {
                "timestamp": timestamp
            }
    except requests.exceptions.ReadTimeout:
        time.sleep(20)
    except requests.exceptions.ConnectionError:
        time.sleep(60)
