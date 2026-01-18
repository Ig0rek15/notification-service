from abc import ABC, abstractmethod

from notifications.models import Notification


class NotificationSender(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> None:
        '''
        Отправляет уведомление.

        Должен:
        - либо завершиться успешно
        - либо выбросить исключение
        '''
        pass
