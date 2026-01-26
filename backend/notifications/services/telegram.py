import requests

from rest_framework import status

from .base import NotificationSender
from .exceptions import (
    RetryableNotificationError,
    NonRetryableNotificationError,
)
from notifications.constants import TELEGRAM_API_URL


class TelegramNotificationSender(NotificationSender):
    def __init__(self, token: str):
        self.token = token

    def send(self, notification):
        if not notification.message:
            raise NonRetryableNotificationError('Empty message')

        try:
            chat_id = int(notification.recipient)
        except ValueError:
            raise NonRetryableNotificationError('Invalid chat_id')

        url = f'{TELEGRAM_API_URL}/bot{self.token}/sendMessage'

        response = requests.post(
            url,
            json={
                'chat_id': chat_id,
                'text': notification.message,
            },
            timeout=5,
        )

        if response.status_code == status.HTTP_200_OK:
            return

        if response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ):
            raise NonRetryableNotificationError(
                f'Telegram API error: {response.text}'
            )

        raise RetryableNotificationError(
            f'Telegram API temporary error: {response.status_code}'
        )
