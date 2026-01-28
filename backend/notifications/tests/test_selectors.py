from notifications.selectors.notification import (
    get_notifications_ready_for_dispatch
)


def test_get_notifications_ready_for_dispatch(scheduled_notification):
    notifications = get_notifications_ready_for_dispatch()

    assert scheduled_notification in notifications
