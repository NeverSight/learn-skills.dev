---
name: erf-build
description: Собрать внешний отчёт 1С (ERF) из XML-исходников
argument-hint: <ReportName>
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# /erf-build — Сборка отчёта

Собирает ERF-файл из XML-исходников с помощью платформы 1С. Использует общий скрипт из `/epf-build`.

## Usage

```
/erf-build <ReportName> [SrcDir] [OutDir]
```

| Параметр   | Обязательный | По умолчанию | Описание                             |
|------------|:------------:|--------------|--------------------------------------|
| ReportName | да           | —            | Имя отчёта (имя корневого XML)       |
| SrcDir     | нет          | `src`        | Каталог исходников                   |
| OutDir     | нет          | `build`      | Каталог для результата               |

## Параметры подключения

Прочитай `.v8-project.json` из корня проекта. Возьми `v8path` (путь к платформе) и разреши базу для сборки:
1. Если пользователь указал параметры подключения (путь, сервер) — используй напрямую
2. Если указал базу по имени — ищи по id / alias / name в `.v8-project.json`
3. Если не указал — сопоставь текущую ветку Git с `databases[].branches`
4. Если ветка не совпала — используй `default`
5. Если `.v8-project.json` нет или баз нет — создай пустую ИБ в `./base`
Если `v8path` не задан — автоопределение: `Get-ChildItem "C:\Program Files\1cv8\*\bin\1cv8.exe" | Sort -Desc | Select -First 1`
Если использованная база не зарегистрирована — после выполнения предложи добавить через `/db-list add`.

## Команда

Используй общий скрипт из epf-build:

```powershell
powershell.exe -NoProfile -File .claude/skills/epf-build/scripts/epf-build.ps1 <параметры>
```

### Параметры скрипта

| Параметр | Обязательный | Описание |
|----------|:------------:|----------|
| `-V8Path <путь>` | нет | Каталог bin платформы (или полный путь к 1cv8.exe) |
| `-InfoBasePath <путь>` | * | Файловая база |
| `-InfoBaseServer <сервер>` | * | Сервер 1С (для серверной базы) |
| `-InfoBaseRef <имя>` | * | Имя базы на сервере |
| `-UserName <имя>` | нет | Имя пользователя |
| `-Password <пароль>` | нет | Пароль |
| `-SourceFile <путь>` | да | Путь к корневому XML-файлу исходников |
| `-OutputFile <путь>` | да | Путь к выходному ERF-файлу |

> `*` — нужен либо `-InfoBasePath`, либо пара `-InfoBaseServer` + `-InfoBaseRef`

## Коды возврата

| Код | Описание                    |
|-----|-----------------------------|
| 0   | Успешная сборка             |
| 1   | Ошибка (см. лог)           |

## Ссылочные типы

Если отчёт использует ссылочные типы конфигурации (`CatalogRef.XXX`, `DocumentRef.XXX`) — сборка в пустой базе упадёт с ошибкой XDTO. Зарегистрируй базу с целевой конфигурацией через `/db-list add`.

## Примеры

```powershell
# Сборка отчёта (файловая база)
powershell.exe -NoProfile -File .claude/skills/epf-build/scripts/epf-build.ps1 -InfoBasePath "C:\Bases\MyDB" -SourceFile "src\МойОтчёт.xml" -OutputFile "build\МойОтчёт.erf"

# Серверная база
powershell.exe -NoProfile -File .claude/skills/epf-build/scripts/epf-build.ps1 -InfoBaseServer "srv01" -InfoBaseRef "MyDB" -UserName "Admin" -Password "secret" -SourceFile "src\МойОтчёт.xml" -OutputFile "build\МойОтчёт.erf"
```
