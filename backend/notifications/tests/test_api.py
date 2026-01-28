import pytest

from rest_framework import status

from notifications.models import NotificationStatus


@pytest.mark.django_db
def test_create_notification(
    api_client,
    email_notification_data,
    mocker,
):
    mocker.patch(
        'notifications.api.views.send_notification.delay',
        return_value=None,
    )

    response = api_client.post(
        '/api/notifications/',
        email_notification_data,
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['status'] == NotificationStatus.QUEUED


@pytest.mark.django_db
def test_get_notification(api_client, notification):
    response = api_client.get(
        f'/api/notifications/{notification.id}/'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == str(notification.id)
