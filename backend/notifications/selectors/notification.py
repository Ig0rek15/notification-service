from django.utils.timezone import now

from notifications.models import Notification, NotificationStatus


def get_notifications_ready_for_dispatch():
    return (
        Notification.objects
        .filter(
            status=NotificationStatus.QUEUED,
            scheduled_at__lte=now()
        )
    )
