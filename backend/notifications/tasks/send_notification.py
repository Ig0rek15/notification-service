import logging

from celery import shared_task
from django.db import transaction

from notifications.constants import MAX_NOTIFICATION_ATTEMPTS
from notifications.models import Notification, NotificationStatus
from notifications.services.factory import get_notification_sender
from notifications.services.exceptions import (
    RetryableNotificationError,
    NonRetryableNotificationError
)

logger = logging.getLogger(__name__)


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

            logger.info(
                'Start processing notification %s (status=%s, attempts=%s)',
                notification.id,
                notification.status,
                notification.attempts,
            )

        try:
            sender = get_notification_sender(notification)
            sender.send(notification)

            with transaction.atomic():
                notification.status = NotificationStatus.SENT
                notification.error = None
                notification.save(update_fields=['status', 'error'])

            logger.info(
                'Notification %s sent successfully',
                notification.id,
            )
            return

        except NonRetryableNotificationError as exc:
            logger.warning(
                'Notification %s failed permanently: %s',
                notification.id,
                exc,
            )

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

            logger.error(
                'Notification %s failed (attempt %s/%s): %s',
                notification.id,
                notification.attempts,
                MAX_NOTIFICATION_ATTEMPTS,
                exc,
            )

            if notification.attempts >= MAX_NOTIFICATION_ATTEMPTS:
                with transaction.atomic():
                    notification.status = NotificationStatus.FAILED
                    notification.save(update_fields=['status'])

                logger.error(
                    'Notification %s marked as FAILED after %s attempts',
                    notification.id,
                    notification.attempts,
                )
                return

            raise self.retry(exc=exc, countdown=2 ** notification.attempts)

    except Notification.DoesNotExist:
        return
