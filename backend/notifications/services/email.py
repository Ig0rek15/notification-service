import os
import smtplib
from email.mime.text import MIMEText

from .base import NotificationSender
from .exceptions import (
    RetryableNotificationError,
    NonRetryableNotificationError,
)


class EmailNotificationSender(NotificationSender):
    def __init__(self):
        self.host = os.getenv('SMTP_HOST')
        self.port = int(os.getenv('SMTP_PORT', 0))
        self.user = os.getenv('SMTP_USER')
        self.password = os.getenv('SMTP_PASSWORD')
        self.use_tls = os.getenv('SMTP_USE_TLS') == 'True'
        self.from_email = os.getenv('SMTP_FROM_EMAIL')

        if not all(
            [self.host, self.port, self.user, self.password, self.from_email]
        ):
            raise NonRetryableNotificationError(
                'SMTP is not fully configured'
            )

    def send(self, notification):
        if not notification.message:
            raise NonRetryableNotificationError('Empty email message')

        if '@' not in notification.recipient:
            raise NonRetryableNotificationError('Invalid email address')

        msg = MIMEText(notification.message)
        msg['Subject'] = notification.subject or 'Notification'
        msg['From'] = self.from_email
        msg['To'] = notification.recipient

        try:
            with smtplib.SMTP(self.host, self.port, timeout=10) as server:
                if self.use_tls:
                    server.starttls()

                server.login(self.user, self.password)
                server.send_message(msg)

        except smtplib.SMTPAuthenticationError as exc:
            raise NonRetryableNotificationError(
                f'SMTP authentication failed: {exc}'
            )

        except smtplib.SMTPException as exc:
            raise RetryableNotificationError(
                f'SMTP temporary error: {exc}'
            )
