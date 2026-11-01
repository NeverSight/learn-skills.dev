---
name: web-stop
description: >
  Этот скилл MUST быть вызван когда пользователь просит остановить веб-сервер, Apache, прекратить веб-публикацию.
  SHOULD также вызывать когда веб-публикации больше не нужны.
  Do NOT использовать для удаления публикаций — используй web-unpublish; для проверки статуса — используй web-info.
argument-hint: ""
allowed-tools:
  - Bash
  - Read
  - Glob
---

# /web-stop — Остановка Apache

Останавливает Apache HTTP Server. Публикации сохраняются — при следующем `/web-publish` сервер запустится снова.

## Usage

```
/web-stop
```

## Параметры подключения

Прочитай `.v8-project.json` из корня проекта. Если задан `webPath` — используй как `-ApachePath`.
По умолчанию `tools/apache24` от корня проекта.

## Команда

```powershell
powershell.exe -NoProfile -File .claude/skills/web-stop/scripts/web-stop.ps1 <параметры>
```

### Параметры скрипта

| Параметр | Обязательный | Описание |
|----------|:------------:|----------|
| `-ApachePath <путь>` | нет | Корень Apache (по умолчанию `tools/apache24`) |

## После выполнения

Предложи пользователю:
- **Перезапуск** — `/web-publish <база>` (повторный вызов поднимет Apache с существующими публикациями)
- **Удаление публикаций** — `/web-unpublish <имя>` или `/web-unpublish --all`

## Примеры

```powershell
# Остановить Apache
powershell.exe -NoProfile -File .claude/skills/web-stop/scripts/web-stop.ps1

# С указанием пути
powershell.exe -NoProfile -File .claude/skills/web-stop/scripts/web-stop.ps1 -ApachePath "C:\tools\apache24"
```
