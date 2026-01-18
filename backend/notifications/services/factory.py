from .email import EmailNotificationSender
from .exceptions import NonRetryableNotificationError
from notifications.models import NotificationChannel


def get_notification_sender(notification):
    if notification.channel == NotificationChannel.EMAIL:
        return EmailNotificationSender()

    raise NonRetryableNotificationError(
        f'Unsupported notification channel: {notification.channel}'
    )
