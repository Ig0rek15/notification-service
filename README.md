# Асинхронный сервис уведомлений

Backend-сервис для асинхронной отправки уведомлений с использованием очередей и фоновых воркеров.

Проект реализован как pet-project:
- асинхронная обработка
- retry-логика
- отложенные задачи
- наблюдаемость через Flower
- Docker-окружение

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

## Архитектура (кратко)

- **Django API**
  - принимает HTTP-запросы
  - валидирует данные
  - сохраняет уведомления в БД
  - ставит задачи в очередь

- **Celery Worker**
  - асинхронно отправляет уведомления
  - управляет retry-логикой
  - обновляет статус уведомлений

- **Celery Beat**
  - периодически проверяет отложенные уведомления
  - диспатчит их в очередь

- **RabbitMQ**
  - брокер сообщений

- **Redis**
  - result backend для Celery

- **Flower**
  - мониторинг воркеров и задач


---

## Структура проекта

```bash
notification-service/
├── backend/
│ ├── project/ # Django project
│ ├── notifications/ # Основное приложение
│ │ ├── api/ # API (serializers, views, urls)
│ │ ├── services/ # Бизнес-логика отправки
│ │ ├── selectors/ # Query-логика (read-only)
│ │ ├── tasks/ # Celery задачи
│ │ ├── models.py
│ ├── manage.py
├── docker-compose.yml
├── .env.example
├── README.md
```


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

```bash
POST /api/notifications/
```

Пример запроса:
```json
{
  "channel": "email",
  "recipient": "user@example.com",
  "message": "Hello from async service"
}
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
