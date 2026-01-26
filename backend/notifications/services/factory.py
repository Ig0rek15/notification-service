import os

from .email import EmailNotificationSender
from .telegram import TelegramNotificationSender
from .exceptions import NonRetryableNotificationError
from notifications.models import NotificationChannel


def get_notification_sender(notification):
    if notification.channel == NotificationChannel.EMAIL:
        return EmailNotificationSender()

    if notification.channel == NotificationChannel.TELEGRAM:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise NonRetryableNotificationError(
                'Telegram bot token is not configured'
            )
        return TelegramNotificationSender(token)

    raise NonRetryableNotificationError(
        f'Unsupported notification channel: {notification.channel}'
    )
