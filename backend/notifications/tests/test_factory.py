import pytest

from notifications.models import Notification
from notifications.services.factory import get_notification_sender
from notifications.services.email import EmailNotificationSender
from notifications.services.exceptions import NonRetryableNotificationError


def test_email_sender_factory(mocker, notification):
    mocker.patch.dict(
        'os.environ',
        {
            'SMTP_HOST': 'smtp.test',
            'SMTP_PORT': '587',
            'SMTP_USER': 'test',
            'SMTP_PASSWORD': 'test',
            'SMTP_FROM_EMAIL': 'test@test.com',
        },
    )

    sender = get_notification_sender(notification)
    assert isinstance(sender, EmailNotificationSender)


def test_unknown_channel_factory(db):
    notification = Notification.objects.create(
        channel='unknown',
        recipient='test',
        message='Hello',
    )

    with pytest.raises(NonRetryableNotificationError):
        get_notification_sender(notification)
