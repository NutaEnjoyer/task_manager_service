# Task Management API

**Task Management API** — это сервис для управления задачами с поддержкой CRUD-операций, уведомлений через Redis и Telegram, автодокументацией и контейнеризацией.

---

## 🚀 Возможности

- **CRUD для задач**: создание, просмотр, обновление, удаление
- **Хранение в PostgreSQL** (через SQLAlchemy)
- **Уведомления через Redis** (pub/sub, отдельный worker)
- **Оповещение в Telegram** при завершении задачи
- **Автогенерируемая документация** (Swagger/OpenAPI)
- **Unit-тесты** для бизнес-логики
- **Контейнеризация** (Docker, docker-compose)
- **Гибкая настройка через .env**

---

## 🗂️ Структура проекта

```
app/
├── api/                # Роуты FastAPI
├── core/               # Конфиги, интеграции
├── models/             # SQLAlchemy-модели
├── schemas/            # Pydantic-схемы
├── services/           # Бизнес-логика
├── redis_pubsub/       # Redis publisher/worker
├── tests/              # Тесты
├── app.py              # Точка входа FastAPI
Dockerfile
docker-compose.yml
.env
README.md
requirements.txt
```

---

## ⚙️ Быстрый старт

### 1. Клонируйте репозиторий

```sh
git clone <ваш-репозиторий>
cd <папка-проекта>
```

### 2. Заполните `.env` по аналогии с `.env.template`

Пример:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/testinfourhours
REDIS_HOST=redis
REDIS_PORT=6379
TELEGRAM_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
```

### 3. Запустите сервисы

```sh
docker-compose up --build
```

- FastAPI: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### 4. Запуск воркера отдельно (если нужно)

```sh
docker-compose run --rm worker
```
или вручную:
```sh
docker-compose exec worker python -m app.redis_pubsub.worker
```

---

## 🧪 Тестирование

```sh
pip install -r requirements.txt
pytest
```

---

## 📝 Примеры запросов

**Создать задачу:**
```http
POST /api/tasks/
{
  "title": "Сделать проект",
  "description": "Сдать до завтра",
  "due_date": "2025-07-02T12:00:00"
}
```

**Обновить статус:**
```http
PUT /api/tasks/1
{
  "status": "done"
}
```

---

## 📦 Миграции БД

```sh
alembic revision --autogenerate -m "Комментарий"
alembic upgrade head
```

