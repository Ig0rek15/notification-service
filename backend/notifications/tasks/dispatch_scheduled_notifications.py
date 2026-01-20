from celery import shared_task

from notifications.selectors.notification import (
    get_notifications_ready_for_dispatch
)
from .send_notification import send_notification


@shared_task
def dispatch_scheduled_notifications() -> None:
    notifications = get_notifications_ready_for_dispatch()

    for notification in notifications:
        send_notification.delay(notification.id)
