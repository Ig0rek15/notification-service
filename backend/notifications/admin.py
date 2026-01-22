from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'channel',
        'recipient',
        'status',
        'attempts',
        'scheduled_at',
        'created_at',
    )

    list_filter = (
        'channel',
        'status',
    )

    search_fields = (
        'recipient',
        'id',
    )

    readonly_fields = (
        'id',
        'channel',
        'recipient',
        'subject',
        'message',
        'status',
        'attempts',
        'error',
        'scheduled_at',
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )

    fieldsets = (
        (
            'Основная информация',
            {
                'fields': (
                    'id',
                    'channel',
                    'recipient',
                    'subject',
                    'message',
                )
            },
        ),
        (
            'Статус доставки',
            {
                'fields': (
                    'status',
                    'attempts',
                    'error',
                    'scheduled_at',
                )
            },
        ),
        (
            'Системные поля',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )
