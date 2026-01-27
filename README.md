# Асинхронный сервис уведомлений

Backend-сервис для асинхронной отправки уведомлений с использованием очередей и фоновых воркеров.


---

## Стек технологий

- Python 3.11
- Django + Django REST Framework
- Celery
- RabbitMQ (broker)
- Redis (result backend)
- PostgreSQL
- Celery Beat (планировщик)
- Flower (мониторинг)
- Docker / Docker Compose

---

## Возможности

- Асинхронная отправка уведомлений
- Поддержка нескольких каналов:
  - Email (SMTP)
  - Telegram Bot
- Retry-логика с backoff
- Отложенные уведомления (`scheduled_at`)
- Хранение статусов и ошибок в БД
- Наблюдаемость через Flower и логи
- Админ-панель для просмотра уведомлений

---

## Переменные окружения

Для запуска проекта необходимо создать файл `.env`
на основе `.env.example`.

Минимальный набор:

```env
# Django
DJANGO_SECRET_KEY='django-insecure-...'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Postgres
POSTGRES_DB=media
POSTGRES_USER=media
POSTGRES_PASSWORD=media
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Celery / RabbitMQ
CELERY_BROKER_URL=amqp://rabbit:rabbit@rabbitmq:5672//

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=True
SMTP_FROM_EMAIL=your_email@gmail.com
```

---

# Запуск проекта
```bash
docker-compose up --build
```

После запуска будут доступны:

- API: http://localhost:8000

- Flower: http://localhost:5555

---

## API
### Создание уведомления

POST /api/notifications/

Поля:
- `channel` — `email` или `telegram`
- `recipient` — email или telegram `chat_id`
- `message` — текст уведомления
- `scheduled_at` (опционально) — дата отправки


---

## Пример запроса

```bash
curl -X POST http://localhost:8000/api/notifications/ \
  -H 'Content-Type: application/json' \
  -d '{
    "channel": "telegram",
    "recipient": "123456789",
    "message": "Hello from async notification service"
  }'
```

Ответ:
```json
{
  "id": "uuid",
  "status": "queued"
}
```

### Получение статуса уведомления
```bash
GET /api/notifications/{id}/
```

Пример ответа:
```json
{
  "id": "uuid",
  "channel": "email",
  "status": "sent",
  "attempts": 0,
  "error": null,
  "created_at": "...",
  "updated_at": "...",
  "scheduled_at": null
}
```

---

## Отложенные уведомления

Если в запросе указать поле scheduled_at,
уведомление будет отправлено не раньше указанного времени.

Пример:
```json
{
  "channel": "email",
  "recipient": "user@example.com",
  "message": "Future message",
  "scheduled_at": "2026-02-01T10:00:00Z"
}
```
