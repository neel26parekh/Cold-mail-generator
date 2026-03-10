import os
import smtplib
from email.message import EmailMessage
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465  # For SSL

    def send_email(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Sends an email using Gmail's SMTP server via SSL.
        """
        if not self.sender_email or not self.app_password:
            logger.error("Missing SENDER_EMAIL or GMAIL_APP_PASSWORD in environment variables.")
            raise ValueError("Email credentials are not configured properly.")

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg.set_content(body)

        try:
            logger.info(f"Attempting to send email to {recipient_email}")
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)
            logger.info(f"Email successfully sent to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}. Error: {str(e)}", exc_info=True)
            raise e
