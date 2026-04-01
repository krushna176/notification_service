
from services.celery_app import celery
from services.email_service import send_email
from services.sms_service import send_sms
from services.push_service import send_push
from utils.logger import get_logger
import asyncio

logger = get_logger("celery.tasks")

@celery.task(bind=True, max_retries=3,name="services.tasks.send_notification")
def send_notification(self, user_data, message):
    try:
        logger.info(f"Processing notification for {user_data}")

        if user_data["pref_email"] and user_data.get("email"):
            logger.info("Sending EMAIL...")
            asyncio.run(send_email(user_data["email"], "Notification", message))
            logger.info("EMAIL SENT...")

        if user_data["pref_sms"] and user_data.get("phone"):
            send_sms(user_data["phone"], message)

        if user_data["pref_push"] and user_data.get("pushover_user_key"):
            send_push(user_data["pushover_user_key"], message)

        logger.info("Notification sent successfully")

    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise self.retry(exc=e, countdown=10)