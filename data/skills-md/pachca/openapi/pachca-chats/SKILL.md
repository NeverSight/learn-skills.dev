---
name: pachca-chats
description: >
  Управление каналами и беседами, участниками чатов. Создание, обновление,
  архивация чатов. Добавление/удаление участников, роли, экспорт сообщений.
  Используй когда нужно: создать канал, добавить участника, архивировать чат,
  найти активные/неактивные чаты, экспорт сообщений. НЕ используй для: отправки
  сообщений (→ pachca-messages).
---

# pachca-chats

Base URL: `https://api.pachca.com/api/shared/v1`
Авторизация: `Authorization: Bearer <ACCESS_TOKEN>`
Токен: бот (Автоматизации → Интеграции → API) или пользователь (Автоматизации → API).
Если токен неизвестен — спроси у пользователя перед выполнением запросов.

## Когда использовать

- создать канал
- создать беседу
- создать чат
- добавить участника
- удалить участника
- архивировать чат
- роли участников
- экспорт сообщений
- список чатов
- активные чаты
- неактивные чаты

## Когда НЕ использовать

- получить профиль, мой профиль, установить статус → **pachca-profile**
- найти сотрудника, создать пользователя, список сотрудников → **pachca-users**
- отправить сообщение, ответить в тред, прикрепить файл → **pachca-messages**
- настроить бота, вебхук, webhook → **pachca-bots**
- показать форму, интерактивная форма, модальное окно → **pachca-forms**
- создать задачу, список задач, напоминание → **pachca-tasks**
- поиск сообщений, найти сообщение, полнотекстовый поиск → **pachca-search**
- аудит, журнал событий, безопасность → **pachca-security**

## Пошаговые сценарии

### Создать канал и пригласить участников

1. POST /chats — `"channel": true` для канала, `false` (по умолчанию) для беседы
2. Участников можно передать сразу при создании: `member_ids` и/или `group_tag_ids` в теле запроса
3. Или добавить позже: POST /chats/{id}/members с `member_ids`, POST /chats/{id}/group_tags с `group_tag_ids`

```bash
curl "https://api.pachca.com/api/shared/v1/chats" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"chat":{"name":"Новый канал","channel":true,"member_ids":[1,2,3]}}'
```

> `channel` — boolean, не строка. `member_ids` и `group_tag_ids` — опциональны при создании.

### Архивация и управление чатом

1. Архивировать: PUT /chats/{id}/archive
2. Разархивировать: PUT /chats/{id}/unarchive
3. Изменить роль участника: PUT /chats/{id}/members/{user_id} с `role` (`"admin"` | `"member"`; `"editor"` — только для каналов). Роль создателя чата изменить нельзя.
4. Удалить участника: DELETE /chats/{id}/members/{user_id}
5. Покинуть чат: DELETE /chats/{id}/leave

### Создать проектную беседу из шаблона

1. POST /chats с `name`, `"channel": false` и `group_tag_ids` (добавить всех участников тега сразу)
2. Или POST /chats → затем POST /chats/{id}/members с `member_ids` + POST /chats/{id}/group_tags с `group_tag_ids`
3. Отправь приветственное сообщение: POST /messages с `"entity_id": chat.id`

```bash
curl "https://api.pachca.com/api/shared/v1/chats" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"chat":{"name":"Проект Alpha","channel":false,"group_tag_ids":[42],"member_ids":[186,187]}}'
```

> `group_tag_ids` при создании добавляет всех участников тега сразу — удобнее, чем добавлять поштучно.

### Экспорт истории чата

1. POST /chats/exports с `start_at`, `end_at` (формат YYYY-MM-DD) и обязательным `webhook_url` — запрос выполняется асинхронно
2. Дождись вебхука на `webhook_url`: придёт JSON с `"type": "export"`, `"event": "ready"` и полем `export_id` — по `"type": "export"` можно отличить от других вебхуков
3. GET /chats/exports/{id} — сервер вернёт 302, большинство HTTP-клиентов скачают файл автоматически

```bash
curl "https://api.pachca.com/api/shared/v1/chats/exports" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"start_at":"$START_DATE","end_at":"$END_DATE","webhook_url":"$WEBHOOK_URL"}'
```

> `webhook_url` обязателен — без него невозможно получить `export_id`. POST не возвращает id в ответе. Экспорт доступен только Владельцу пространства на тарифе «Корпорация». Максимальный период: 45 дней (366 дней при указании конкретных чатов).

### Найти активные чаты за период

1. GET /chats с `last_message_at_after={дата}` — только чаты с активностью после указанной даты
2. Для диапазона добавь `last_message_at_before={дата}` — чаты с активностью между двумя датами
3. Перебери страницы: `cursor` из `meta.paginate.next_page`, пока он не пустой

```bash
curl "https://api.pachca.com/api/shared/v1/chats?last_message_at_after=$DATE_FROM&limit=50" \
  -H "Authorization: Bearer $TOKEN"
```

> Дата в формате ISO-8601 UTC+0: `YYYY-MM-DDThh:mm:ss.sssZ`. Для «последних N дней» вычисли `now - N days` в UTC.

### Найти и заархивировать неактивные чаты

1. GET /chats с `last_message_at_before={порог}` — сразу только чаты без активности с нужной даты
2. Перебери страницы: `cursor` из `meta.paginate.next_page`, пока он не пустой
3. Для каждого чата: PUT /chats/{id}/archive

```bash
curl "https://api.pachca.com/api/shared/v1/chats?last_message_at_before=$DATE_BEFORE&limit=50" \
  -H "Authorization: Bearer $TOKEN"
```

> Проверяй `"channel": false` — архивация каналов может быть нежелательной. Уточняй у владельца перед массовой архивацией.

## Обработка ошибок

| Код | Причина | Что делать |
|-----|---------|------------|
| 422 | Неверные параметры | Проверь обязательные поля, типы данных, допустимые значения enum |
| 429 | Rate limit | Подожди и повтори. Лимит: ~50 req/sec, сообщения ~4 req/sec |
| 403 | Нет доступа | Недостаточно скоупов (`insufficient_scope`), бот не в чате, или endpoint только для админов/владельцев |
| 404 | Не найдено | Неверный id. Проверь что сущность существует |
| 401 | Не авторизован | Проверь токен в заголовке Authorization |

## Доступные операции

### Новый чат

`POST /chats`

> скоуп: `chats:create`

```json
{
  "chat": {
    "name": ""
  }
}
```

### Список чатов

`GET /chats`

> скоуп: `chats:read`

### Экспорт сообщений

`POST /chats/exports`

> скоуп: `chat_exports:write` · тариф: **Корпорация**

```json
{
  "start_at": "2025-03-20",
  "end_at": "2025-03-20",
  "webhook_url": "https://webhook.site/9227d3b8-6e82-4e64-bf5d-ad972ad270f2"
}
```

### Скачать архив экспорта

`GET /chats/exports/{id}`

> скоуп: `chat_exports:read` · тариф: **Корпорация**

### Информация о чате

`GET /chats/{id}`

> скоуп: `chats:read`

### Обновление чата

`PUT /chats/{id}`

> скоуп: `chats:update`

```json
{
  "chat": {}
}
```

### Архивация чата

`PUT /chats/{id}/archive`

> скоуп: `chats:archive`

### Добавление тегов

`POST /chats/{id}/group_tags`

> скоуп: `chat_members:write`

```json
{
  "group_tag_ids": [
    86,
    18
  ]
}
```

### Исключение тега

`DELETE /chats/{id}/group_tags/{tag_id}`

> скоуп: `chat_members:write`

### Выход из беседы или канала

`DELETE /chats/{id}/leave`

> скоуп: `chats:leave`

### Список участников чата

`GET /chats/{id}/members`

> скоуп: `chat_members:read`

### Добавление пользователей

`POST /chats/{id}/members`

> скоуп: `chat_members:write`

```json
{
  "member_ids": [
    186,
    187
  ]
}
```

### Исключение пользователя

`DELETE /chats/{id}/members/{user_id}`

> скоуп: `chat_members:write`

### Редактирование роли

`PUT /chats/{id}/members/{user_id}`

> скоуп: `chat_members:write`

```json
{
  "role": "admin"
}
```

### Разархивация чата

`PUT /chats/{id}/unarchive`

> скоуп: `chats:archive`

## Ограничения и gotchas

- `role`: допустимые значения — `admin` (Админ), `editor` (Редактор (доступно только для каналов)), `member` (Участник или подписчик)
- `limit`: максимум 50
- Пагинация: cursor-based (limit + cursor), НЕ page-based

## Подробнее

см. [references/endpoints.md](references/endpoints.md)
