import uuid


from django.db import models

# Create your models here.


class Notification(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    channel = models.CharField(max_length=64)
    recipient = models.CharField(max_length=64)
    subject = None
    message = models.TextField()
    status = models.CharField(max_length=32)
    attempts = models.PositiveSmallIntegerField(default=0,)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
