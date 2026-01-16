import time

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from .models import Notification, NotificationStatus


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3}
)
def send_notification(self, notification_id: str) -> None:
    try:
        with transaction.atomic():
            notification = Notification.objects.select_for_update().get(id=notification_id)
            notification.status = NotificationStatus.PROCESSING
            notification.attempts += 1
            notification.save(update_fields=['status'])
    except ObjectDoesNotExist:
        return

    time.sleep(3)

    with transaction.atomic():
        notification = Notification.objects.select_for_update(
            ).get(id=notification_id)
        notification.status = NotificationStatus.SENT
        notification.save(update_fields=['status'])
