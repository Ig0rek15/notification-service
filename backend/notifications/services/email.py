from .base import NotificationSender
from .exceptions import NonRetryableNotificationError


class EmailNotificationSender(NotificationSender):
    def send(self, notification):
        if not notification.message:
            raise NonRetryableNotificationError('Empty message')

        if '@' not in notification.recipient:
            raise NonRetryableNotificationError('Invalid email')

        # тут позже будет SMTP (Наверно)
        return
