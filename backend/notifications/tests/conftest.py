import pytest

from django.utils.timezone import now, timedelta
from rest_framework.test import APIClient

from notifications.models import Notification, NotificationStatus


@pytest.fixture
def email_notification_data():
    return {
        'channel': 'email',
        'recipient': 'user@example.com',
        'message': 'Test message',
    }


@pytest.fixture
def notification(db, email_notification_data):
    return Notification.objects.create(
        **email_notification_data,
        status=NotificationStatus.QUEUED,
    )


@pytest.fixture
def scheduled_notification(db, email_notification_data):
    return Notification.objects.create(
        **email_notification_data,
        status=NotificationStatus.QUEUED,
        scheduled_at=now() - timedelta(minutes=1),
    )


@pytest.fixture
def api_client():
    return APIClient()
