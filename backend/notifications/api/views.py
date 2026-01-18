from rest_framework import viewsets, mixins
from rest_framework.response import Response

from notifications.models import Notification
from .serializers import NotificationSerializer
from notifications.tasks.send_notification import send_notification


class NotificationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification = serializer.save()

        send_notification.delay(notification.id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
