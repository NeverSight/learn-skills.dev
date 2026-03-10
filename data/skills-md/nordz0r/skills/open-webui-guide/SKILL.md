---
name: open-webui-guide
description: "Подробная русскоязычная справка по Open WebUI: архитектура, авторизация, функции, пайплайны, API, RAG, масштабирование, отладка и скрытые возможности. Используй этот скилл при любых вопросах об Open WebUI — как он устроен, как развернуть, настроить авторизацию (OAuth, LDAP, JWT), написать функцию или пайплайн, подключить модель (Ollama, OpenAI), настроить RAG/knowledge base, масштабировать на production, отладить проблему. Также используй при написании кода для Open WebUI: функции (filter, pipe, action), пайплайны, конфигурации, docker-compose."
---

# Open WebUI — Полная справка (RU)

Этот скилл — исчерпывающий русскоязычный справочник по Open WebUI. Он покрывает архитектуру, все ключевые подсистемы и практические рецепты.

## Структура проекта

```
open-webui/
├── backend/open_webui/          # Python-бэкенд (FastAPI)
│   ├── main.py                  # Точка входа приложения
│   ├── env.py                   # Переменные окружения
│   ├── config.py                # Конфигурация приложения
│   ├── routers/                 # API-роутеры (27+ модулей)
│   ├── models/                  # SQLAlchemy ORM-модели (23+ таблиц)
│   ├── socket/main.py           # WebSocket (Socket.IO)
│   ├── utils/                   # Утилиты, хелперы
│   └── apps/                    # Вспомогательные приложения
├── src/                         # SvelteKit-фронтенд
│   ├── routes/                  # Страницы и маршруты
│   ├── lib/components/          # UI-компоненты
│   └── lib/apis/                # API-клиенты
├── Dockerfile                   # Multi-stage сборка
├── docker-compose.yaml          # Развёртывание с Ollama
└── pyproject.toml               # Python-зависимости (uv)
```

## Архитектура

Open WebUI — это полнофункциональный веб-интерфейс для LLM. Ключевые характеристики:

- **Бэкенд**: FastAPI (Python 3.11+), асинхронный
- **Фронтенд**: SvelteKit + TailwindCSS
- **БД**: SQLite (по умолчанию) / PostgreSQL / MySQL через SQLAlchemy
- **Кэш/очереди**: Redis (опционально, нужен для масштабирования)
- **Реалтайм**: Socket.IO (WebSocket) с поддержкой Redis-адаптера
- **Векторная БД**: Chroma (по умолчанию) / Milvus / Weaviate / Qdrant / OpenSearch / Pgvector
- **LLM-провайдеры**: Ollama, OpenAI-совместимые API, любые через пайплайны

## Навигация по справке

В зависимости от вопроса, обращайся к соответствующему справочному файлу:

| Тема | Файл | Когда читать |
|------|------|-------------|
| Авторизация и доступ | `references/auth.md` | JWT, OAuth, LDAP, API-ключи, роли, права |
| Функции | `references/functions.md` | Создание filter/pipe/action, valves, примеры кода |
| Пайплайны | `references/pipelines.md` | Внешние сервисы обработки, отличие от функций |
| API-эндпоинты | `references/api.md` | Полный список роутеров и эндпоинтов |
| Конфигурация | `references/config.md` | Переменные окружения, настройка |
| Масштабирование | `references/scaling.md` | Production-деплой, Redis, PostgreSQL, HA |
| База данных | `references/database.md` | ORM-модели, таблицы, миграции |
| RAG и Knowledge | `references/rag.md` | Базы знаний, эмбеддинги, поиск |
| WebSocket | `references/websocket.md` | Реалтайм, Socket.IO, события |
| Отладка | `references/troubleshooting.md` | Типичные проблемы и их решения |
| Скрытые возможности | `references/hidden.md` | Неочевидные фичи, Easter eggs, продвинутые настройки |

## Быстрый старт

### Запуск через Docker (рекомендуется)

```bash
# С Ollama (локальные модели)
docker compose up -d

# Только Open WebUI (внешний LLM-провайдер)
docker run -d -p 3000:8080 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

### Запуск для разработки

```bash
# Бэкенд
cd backend
pip install -e ".[dev]"
bash start.sh

# Фронтенд
npm install
npm run dev
```

### Первый вход

При первом запуске создаётся учётная запись администратора. Первый зарегистрированный пользователь автоматически получает роль `admin`. Чтобы задать admin-аккаунт заранее:

```env
WEBUI_ADMIN_EMAIL=admin@example.com
WEBUI_ADMIN_NAME=Admin
```

## Ключевые концепции

### Роли пользователей

- **admin** — полный доступ: управление пользователями, моделями, функциями, настройками
- **user** — стандартный пользователь, может общаться с моделями в рамках своих прав
- **pending** — новый пользователь, ожидающий одобрения администратором

### Модели

Open WebUI — это агрегатор моделей. Он подключается к:
- **Ollama** — локальные модели (llama, mistral, и т.д.)
- **OpenAI API** — GPT-4, GPT-3.5 и совместимые (vLLM, LiteLLM, и т.д.)
- **Пайплайны** — кастомные провайдеры через HTTP

Администратор может создавать «модельные карточки» — кастомные обёртки с системным промптом, параметрами и привязкой к базовой модели.

### Функции vs Пайплайны

Это два разных механизма расширения — подробности в `references/functions.md` и `references/pipelines.md`. Кратко:

- **Функции** — Python-код, исполняемый *внутри* Open WebUI. Три типа: filter (пре/пост-обработка), pipe (кастомный провайдер), action (действие по кнопке).
- **Пайплайны** — *внешние* HTTP-сервисы. Open WebUI шлёт запросы к ним по REST. Отдельный процесс/контейнер.

### Knowledge/RAG

Базы знаний позволяют моделям отвечать на основе загруженных документов:
1. Загрузи файлы (PDF, DOCX, TXT, MD и др.)
2. Open WebUI разбивает их на чанки и создаёт эмбеддинги
3. При вопросе система находит релевантные чанки и добавляет их в контекст модели

Подробности в `references/rag.md`.

## Помощь с кодом

При написании кода для Open WebUI (функции, пайплайны, кастомизация):

1. Сначала прочитай `references/functions.md` или `references/pipelines.md` для понимания структуры
2. Посмотри существующие примеры в `backend/open_webui/functions/` если они есть
3. При отладке смотри `references/troubleshooting.md`

## Отладка

При возникновении проблем:

1. Включи подробное логирование: `GLOBAL_LOG_LEVEL=DEBUG`
2. Проверь `references/troubleshooting.md` — там собраны типичные ошибки
3. Для проблем с авторизацией — `references/auth.md`
4. Для проблем с моделями — проверь подключение к Ollama/OpenAI
5. Для проблем с RAG — `references/rag.md`
