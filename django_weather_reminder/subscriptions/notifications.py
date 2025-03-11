import logging

import requests
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def send_email_notification(to_email, subject, message):
    logger.info(f"Sending email to: {to_email}")
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False
        )
        logger.info(f"Email sent to: {to_email}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")

def send_webhook_notification(webhook_url, payload):
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Webhook Error: {e}")
