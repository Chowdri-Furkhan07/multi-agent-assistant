"""Notifier agent: sends the assistant's results via email (SMTP)."""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_TIMEOUT = 10  # seconds


class NotifierAgentError(Exception):
    """Raised when an email could not be sent."""


def send_email(to_email: str, subject: str, message: str) -> None:
    """Send ``message`` to ``to_email`` via Gmail SMTP.

    Requires ``EMAIL_SENDER`` and ``EMAIL_PASSWORD`` (a Gmail App
    Password, not your account password) to be set as environment
    variables.

    Raises:
        NotifierAgentError: if credentials are missing or sending fails.
    """
    sender_email = os.getenv("EMAIL_SENDER")
    app_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not app_password:
        raise NotifierAgentError(
            "EMAIL_SENDER or EMAIL_PASSWORD not set in environment variables"
        )

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
        logger.info("Email sent to %s", to_email)
    except smtplib.SMTPException as exc:
        logger.exception("Failed to send email")
        raise NotifierAgentError(f"Failed to send email: {exc}") from exc


if __name__ == "__main__":
    send_email(
        to_email=os.getenv("TEST_RECIPIENT_EMAIL", "your_email@example.com"),
        subject="Test Email from Agentic AI Assistant",
        message="Hello! This is a test email from your Agentic AI system.",
    )
