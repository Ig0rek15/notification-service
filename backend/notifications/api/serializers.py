from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    scheduled_at = serializers.DateTimeField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Notification
        fields = (
            'id',
            'channel',
            'recipient',
            'message',
            'status',
            'attempts',
            'error',
            'created_at',
            'updated_at',
            'scheduled_at',
        )
        read_only_fields = (
            'status',
            'attempts',
            'error',
            'created_at',
            'updated_at',
        )
