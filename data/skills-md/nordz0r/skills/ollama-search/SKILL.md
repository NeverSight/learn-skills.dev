---
name: ollama-search
description: "Полная русскоязычная справка по Ollama Web Search и Web Fetch API: поиск в интернете, получение контента страниц, Python/JS SDK, MCP-сервер, интеграция с OpenClaw. Используй этот скилл при любых вопросах об Ollama web search — как настроить API-ключ, выполнить поиск, получить содержимое страницы, подключить SDK, настроить MCP-сервер, интегрировать с агентами. Также используй при написании кода для Ollama search: bash-скрипты, Python asyncio, JS/TS клиенты, tool-calling агенты, конфигурация OpenClaw. Триггерится на слова: ollama search, ollama web search, ollama_search, ollama fetch, web_search ollama, ollama api key, ollama MCP, поиск через ollama."
metadata: {"openclaw":{"requires":{"bins":["bash","curl","jq"],"env":["OLLAMA_SEARCH_API_KEY"]}}}
---

# Ollama Search — веб-поиск и получение контента

Скилл для работы с Ollama Web Search API — hosted-сервисом поиска в интернете и извлечения контента страниц. Не требует локального запуска Ollama; работает через облачный API с авторизацией по ключу.

## Навигация по справке

| Тема | Файл | Когда читать |
|------|------|-------------|
| REST API (endpoints, параметры, ответы) | `references/api.md` | Нужны детали запросов, форматы ответов, коды ошибок |
| Python и JS SDK | `references/sdk.md` | Пишешь код на Python или JavaScript/TypeScript |
| MCP-сервер | `references/mcp.md` | Подключаешь Ollama Search к IDE, агентам или другим MCP-клиентам |
| Конфигурация OpenClaw | `references/config.md` | Настраиваешь скилл в OpenClaw, диагностируешь проблемы |

## Быстрый старт

### 1. Получи API-ключ

Зарегистрируйся на [ollama.com](https://ollama.com) и создай ключ: **Settings → API Keys** (`https://ollama.com/settings/keys`).

### 2. Установи переменную окружения

```bash
export OLLAMA_SEARCH_API_KEY="your-key-here"
```

### 3. Проверь работу

```bash
# Поиск
bash {baseDir}/scripts/ollama-search.sh --query "что такое OpenClaw"

# Получение контента страницы
bash {baseDir}/scripts/ollama-fetch.sh --url "https://example.com"
```

## Два API-эндпоинта

### Web Search — поиск по интернету

```
POST https://ollama.com/api/web_search
```

Принимает `query` (строка) и `max_results` (1–10, по умолчанию 5). Возвращает массив результатов с `title`, `url`, `content`.

### Web Fetch — получение контента страницы

```
POST https://ollama.com/api/web_fetch
```

Принимает `url` (строка). Возвращает `title`, `content` (основной текст) и `links` (найденные ссылки).

Оба эндпоинта требуют заголовок `Authorization: Bearer $OLLAMA_SEARCH_API_KEY`.

## Скрипты

Скилл включает два готовых bash-скрипта в `scripts/`:

### ollama-search.sh

```bash
bash {baseDir}/scripts/ollama-search.sh --query "запрос" [--max-results 3] [--json]
```

- `--query` — текст поискового запроса (обязательно)
- `--max-results` — количество результатов, 1–10 (по умолчанию 5)
- `--json` — вывод в сыром JSON вместо таблицы

### ollama-fetch.sh

```bash
bash {baseDir}/scripts/ollama-fetch.sh --url "https://example.com" [--json] [--links]
```

- `--url` — URL страницы (обязательно)
- `--json` — полный JSON-ответ
- `--links` — показать найденные ссылки

## Рабочий процесс для агента

1. Пользователь просит найти информацию → используй `ollama-search.sh`
2. Нужно раскрыть конкретную ссылку из результатов → используй `ollama-fetch.sh`
3. Суммаризируй результаты своими словами, не копируй сырой JSON (если пользователь явно не просит)
4. Если запрос широкий — используй `--max-results 8-10`; для точного — `--max-results 3`

### Пример цепочки: поиск → чтение

```bash
# 1. Ищем
bash {baseDir}/scripts/ollama-search.sh --query "ollama web search api docs" --max-results 3

# 2. Читаем самый релевантный результат
bash {baseDir}/scripts/ollama-fetch.sh --url "https://docs.ollama.com/capabilities/web-search"
```

## SDK и программная интеграция

Для Python и JavaScript/TypeScript есть официальные SDK. Подробности и примеры в `references/sdk.md`.

**Python (быстрый пример):**

```python
import ollama

results = ollama.web_search("что нового в ollama")
page = ollama.web_fetch("https://example.com")
```

**JavaScript:**

```javascript
import { Ollama } from "ollama";
const client = new Ollama();
const results = await client.webSearch("query");
const page = await client.webFetch("https://example.com");
```

## MCP-сервер

Ollama предоставляет MCP-сервер для интеграции поиска с IDE и агентами (Cline, Codex, Goose, Claude Code и др.). Подробности настройки в `references/mcp.md`.

## Безопасность

- Не передавай секреты в поисковых запросах
- Скрипты только читают данные (read-only) — ничего не модифицируют
- API-ключ передаётся через переменную окружения `OLLAMA_SEARCH_API_KEY`, не хардкодь в скриптах
- При использовании в OpenClaw, ключ хранится в `openclaw.json` → `.skills.entries.ollama_search.env`
