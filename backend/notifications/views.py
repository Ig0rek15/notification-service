from rest_framework import viewsets, mixins

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
