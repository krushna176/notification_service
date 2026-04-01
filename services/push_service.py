
import requests
from utils.logger import get_logger
from decouple import config

logger = get_logger("services.push")

APP_TOKEN = config('ACCOUNT_SID')

def send_push(user_key: str, message: str):
    try:
        logger.info(f"Sending push to {user_key}")

        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": APP_TOKEN,
            "user": user_key,
            "message": message
        })

        logger.info("Push sent")

    except Exception as e:
        logger.error(f"Push failed: {str(e)}")
        raise