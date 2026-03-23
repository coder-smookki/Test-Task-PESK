![CI](https://github.com/coder-smookki/Test-Task-PESK/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/coder-smookki/Test-Task-PESK/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![License](https://img.shields.io/github/license/coder-smookki/Test-Task-PESK)

# Test-Task-PESK

Веб-сервис и Telegram-бот для получения информации о любом городе: погода, курс валюты, координаты.

---

## Запуск локально

### 1. Переменные окружения

```bash
cp .env.example .env
# заполнить BOT_TOKEN, OWM_API_KEY, EXCHANGE_API_KEY
```

### 2. Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[api]"
```

### 3. Запуск API + сайта

```bash
python -m app.api
```

Открыть: [http://localhost:8000](http://localhost:8000)
Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Запуск бота

```bash
pip install -e .
python -m app.bot
```

### 5. Тесты

```bash
pip install -e ".[api,dev]"
pytest tests/ -v
```

---

## Запуск через Docker

```bash
cp .env.example .env
# заполнить .env

docker compose up -d
```

| Сервис | URL |
|--------|-----|
| Сайт | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Health | http://localhost:8000/api/v1/health |

Остановить:

```bash
docker compose down
```
