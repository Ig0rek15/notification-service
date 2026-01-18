class NotificationError(Exception):
    '''Базовое исключение доставки'''
    pass


class RetryableNotificationError(NotificationError):
    '''Временная ошибка — можно повторить'''
    pass


class NonRetryableNotificationError(NotificationError):
    '''Фатальная ошибка — повтор бессмысленен'''
    pass
