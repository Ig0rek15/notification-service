import uuid

from django.db import models


class NotificationStatus(models.TextChoices):
    QUEUED = 'queued', 'Queued'
    PROCESSING = 'processing', 'Processing'
    SENT = 'sent', 'Sent'
    FAILED = 'failed', 'Failed'


class NotificationChannel(models.TextChoices):
    EMAIL = 'email', 'Email'
    TELEGRAM = 'telegram', 'Telegram'
    SMS = 'sms', 'SMS'
    VK = 'vk', 'VK'


class Notification(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    channel = models.CharField(
        max_length=32,
        choices=NotificationChannel.choices
    )
    recipient = models.CharField(max_length=64)
    subject = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    message = models.TextField()
    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Когда уведомление должно быть отправлено'
    )
    status = models.CharField(
        max_length=32,
        choices=NotificationStatus.choices,
        default=NotificationStatus.QUEUED
    )
    attempts = models.PositiveSmallIntegerField(default=0,)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
