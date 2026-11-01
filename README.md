# Project For Every Projects

Универсальная стартовая заготовка для небольших backend, full-stack и ML-проектов на FastAPI.

Основная цель проекта — не писать каждый раз инфраструктуру с нуля, а иметь готовый шаблон с подключённой базой данных, миграциями, Docker Compose, API и простым frontend.

## Стек

- Python 3.12
- FastAPI
- SQLAlchemy
- asyncpg
- PostgreSQL
- Alembic
- Docker
- Docker Compose
- nginx
- HTML / CSS / JavaScript
- uv

## Архитектура

```text
Browser
   |
   v
Frontend / nginx
   |
   | /api/*
   v
FastAPI
   |
   v
PostgreSQL

   +
Alembic migrations
```

Сервисы запускаются в следующем порядке:

```text
PostgreSQL
    |
    v
healthcheck базы данных
    |
    v
Alembic migrations
    |
    v
FastAPI
    |
    v
healthcheck API
    |
    v
Frontend
```

## Структура проекта

```text
.
├── app/
│   ├── alembic/
│   │   └── versions/
│   ├── api/
│   │   ├── health.py
│   │   └── router.py
│   ├── core/
│   │   ├── models/
│   │   └── config.py
│   ├── utils/
│   ├── alembic.ini
│   └── main.py
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Что уже настроено

### PostgreSQL

PostgreSQL запускается в отдельном Docker-контейнере.

Для хранения данных используется Docker volume, поэтому данные базы не исчезают после обычного перезапуска контейнеров.

### Alembic

Alembic используется для управления миграциями базы данных.

Перед запуском FastAPI отдельный контейнер выполняет:

```bash
alembic upgrade head
```

API запускается только после успешного выполнения миграций.

### FastAPI

Backend работает на FastAPI.

По умолчанию API доступно по адресу:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Frontend

Frontend пока является простой заглушкой на HTML, CSS и JavaScript.

Он запускается через nginx:

```text
http://localhost:8080
```

nginx также проксирует запросы:

```text
/api/*
```

в контейнер FastAPI.

Благодаря этому frontend может обращаться к backend через обычные относительные URL:

```text
/api/v1/health/ready
```

без отдельной настройки CORS.

### Adminer

Adminer используется как дополнительный интерфейс для просмотра PostgreSQL.

Он вынесен в отдельный Docker Compose profile и не запускается вместе с основным приложением без необходимости.

---

## Переменные окружения

В корне проекта необходимо создать `.env`:

```dotenv
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=app
```

Настоящий `.env` не должен попадать в Git.

Для примера используется:

```text
.env.example
```

Настройки FastAPI загружаются через Pydantic Settings.

Пример URL подключения к PostgreSQL внутри Docker:

```dotenv
APP_CONFIG__DB__URL=postgresql+asyncpg://app:app@db:5432/app
```

`db` — это имя PostgreSQL-сервиса в `docker-compose.yml`.

Docker Compose позволяет контейнерам обращаться друг к другу по имени сервиса.

---

## Запуск проекта

Собрать и запустить все контейнеры:

```bash
docker compose up --build -d
```

Или через Makefile:

```bash
make up
```

Проверить состояние контейнеров:

```bash
docker compose ps
```

Пример ожидаемого состояния:

```text
db         Up (healthy)
migrate    Exited (0)
api        Up (healthy)
frontend   Up
```

Контейнер `migrate` должен завершиться после выполнения миграций.

Статус:

```text
Exited (0)
```

означает успешное выполнение.

---

## Healthcheck

### Liveness

Проверяет, что FastAPI запущен и отвечает:

```text
GET /api/v1/health/live
```

Проверка:

```bash
curl http://localhost:8000/api/v1/health/live
```

Ответ:

```json
{
  "status": "ok"
}
```

### Readiness

Проверяет не только FastAPI, но и соединение с PostgreSQL:

```text
GET /api/v1/health/ready
```

Проверка:

```bash
curl http://localhost:8000/api/v1/health/ready
```

Ответ:

```json
{
  "status": "ok",
  "database": "available"
}
```

Ту же ручку можно вызвать через nginx:

```bash
curl http://localhost:8080/api/v1/health/ready
```

Таким образом проверяется вся цепочка:

```text
Client
  ↓
nginx
  ↓
FastAPI
  ↓
PostgreSQL
```

---

## Swagger

FastAPI автоматически генерирует документацию API.

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI schema:

```text
http://localhost:8000/openapi.json
```

---

## Миграции

Создать новую миграцию:

```bash
cd app

alembic revision --autogenerate -m "migration description"
```

Применить миграции:

```bash
alembic upgrade head
```

Откатить последнюю миграцию:

```bash
alembic downgrade -1
```

При запуске через Docker Compose существующие миграции применяются автоматически сервисом `migrate`.

---

## Adminer

Запустить дополнительные инструменты:

```bash
docker compose --profile tools up -d
```

Для подключения к PostgreSQL из Adminer:

```text
Server: db
Database: app
Username: app
Password: app
```

---

## Логи

Все сервисы:

```bash
docker compose logs -f
```

FastAPI:

```bash
docker compose logs -f api
```

PostgreSQL:

```bash
docker compose logs -f db
```

Миграции:

```bash
docker compose logs migrate
```

Frontend:

```bash
docker compose logs -f frontend
```

---

## Остановка проекта

```bash
docker compose down
```

Или:

```bash
make down
```

---

## Полный сброс базы данных

Удалить контейнеры вместе с PostgreSQL volume:

```bash
docker compose down -v
```

После этого можно заново поднять проект:

```bash
docker compose up --build -d
```

> Команда `docker compose down -v` удаляет данные PostgreSQL.

---

## Для чего нужен этот проект

Этот репозиторий не привязан к конкретной бизнес-логике.

Это базовый шаблон, который можно использовать как фундамент для следующих проектов.

Например:

- REST API;
- CRUD-приложение;
- небольшой full-stack проект;
- сервис авторизации;
- dashboard;
- ML inference API;
- сервис обработки данных;
- учебный или pet project.

Вместо повторной настройки:

```text
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Docker
nginx
healthchecks
```

можно взять готовый шаблон и сразу заниматься логикой конкретного приложения.

Например:

```text
Template
   |
   +-- Todo App
   |
   +-- Notes App
   |
   +-- ML Service
   |
   +-- Dashboard
   |
   +-- REST API
```

## Текущее состояние

На данный момент проект предоставляет базовую инфраструктуру:

```text
FastAPI
   +
PostgreSQL
   +
async SQLAlchemy
   +
Alembic
   +
Docker Compose
   +
healthchecks
   +
nginx
   +
frontend-заглушка
```

Бизнес-логика намеренно минимальна.

Дальнейшая разработка конкретного приложения заключается в добавлении своих моделей базы данных, API-ручек, сервисов и frontend-компонентов поверх уже готовой инфраструктуры.