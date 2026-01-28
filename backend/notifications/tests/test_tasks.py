import pytest
from notifications.models import NotificationStatus
from notifications.tasks.send_notification import send_notification
from notifications.services.exceptions import NonRetryableNotificationError


@pytest.mark.django_db
def test_send_notification_success(mocker, notification):
    mocker.patch(
        'notifications.services.email.EmailNotificationSender.send',
        return_value=None,
    )

    send_notification(notification.id)

    notification.refresh_from_db()
    assert notification.status == NotificationStatus.SENT


@pytest.mark.django_db
def test_send_notification_non_retryable_error(mocker, notification):
    mocker.patch(
        'notifications.services.email.EmailNotificationSender.send',
        side_effect=NonRetryableNotificationError('fail'),
    )

    send_notification(notification.id)

    notification.refresh_from_db()
    assert notification.status == NotificationStatus.FAILED
