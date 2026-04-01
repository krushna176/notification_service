from twilio.rest import Client
from decouple import config
from utils.logger import get_logger

logger = get_logger("services.sms")


ACCOUNT_SID = config('ACCOUNT_SID')
AUTH_TOKEN = config('AUTH_TOKEN')
FROM_NUMBER = config('FROM_NUMBER')

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def format_phone(phone: str):
    if not phone.startswith("+"):
        return "+91" + phone  # assuming India
    return phone



def send_sms(to_phone: str, message: str):
    try:
        logger.info(f"Sending SMS to {to_phone}")

        client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=format_phone(to_phone)
    )

        logger.info("SMS sent")

    except Exception as e:
        logger.error(f"SMS failed: {str(e)}")
        raise