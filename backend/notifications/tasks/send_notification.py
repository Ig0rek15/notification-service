from celery import shared_task
from django.db import transaction

from notifications.constants import MAX_NOTIFICATION_ATTEMPTS
from notifications.models import Notification, NotificationStatus
from notifications.services.factory import get_notification_sender
from notifications.services.exceptions import (
    RetryableNotificationError,
    NonRetryableNotificationError
)


@shared_task(bind=True, max_retries=MAX_NOTIFICATION_ATTEMPTS)
def send_notification(self, notification_id: str) -> None:
    try:
        with transaction.atomic():
            notification = (
                Notification.objects
                .select_for_update()
                .get(id=notification_id)
            )

            if notification.status in (
                NotificationStatus.SENT,
                NotificationStatus.FAILED,
            ):
                return

            notification.status = NotificationStatus.PROCESSING
            notification.save(update_fields=['status'])

        try:
            sender = get_notification_sender(notification)
            sender.send(notification)

            with transaction.atomic():
                notification.status = NotificationStatus.SENT
                notification.error = None
                notification.save(update_fields=['status', 'error'])
            return

        except NonRetryableNotificationError as exc:
            with transaction.atomic():
                notification.attempts += 1
                notification.status = NotificationStatus.FAILED
                notification.error = str(exc)
                notification.save(
                    update_fields=['attempts', 'status', 'error']
                )
            return

        except RetryableNotificationError as exc:
            with transaction.atomic():
                notification.attempts += 1
                notification.error = str(exc)
                notification.save(update_fields=['attempts', 'error'])

            if notification.attempts >= MAX_NOTIFICATION_ATTEMPTS:
                with transaction.atomic():
                    notification.status = NotificationStatus.FAILED
                    notification.save(update_fields=['status'])
                return

            raise self.retry(exc=exc, countdown=2 ** notification.attempts)

    except Notification.DoesNotExist:
        return
