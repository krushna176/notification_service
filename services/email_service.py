import aiosmtplib
from email.message import EmailMessage
from decouple import config
from utils.logger import get_logger

logger = get_logger("services.email")

from_email = config('FROM_EMAIL')
from_email_pw = config('FROM_EMAIL_PW')


async def send_email(to_email: str, subject: str, message: str):
    try:
        logger.info(f"Sending email to {to_email}")

        msg = EmailMessage()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(message)

        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=from_email,
            password=from_email_pw
        )

        logger.info(f"Email sent to {to_email}")

    except Exception as e:
        logger.error(f"Email failed: {str(e)}")
        raise