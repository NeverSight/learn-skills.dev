---
name: epf-build
description: Собрать внешнюю обработку 1С (EPF/ERF) из XML-исходников
argument-hint: <ProcessorName>
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# /epf-build — Сборка обработки

Собирает EPF-файл из XML-исходников с помощью платформы 1С. Та же команда CLI работает и для внешних отчётов (ERF) — см. `/erf-build`.

## Usage

```
/epf-build <ProcessorName> [SrcDir] [OutDir]
```

| Параметр      | Обязательный | По умолчанию | Описание                             |
|---------------|:------------:|--------------|--------------------------------------|
| ProcessorName | да           | —            | Имя обработки (имя корневого XML)    |
| SrcDir        | нет          | `src`        | Каталог исходников                   |
| OutDir        | нет          | `build`      | Каталог для результата               |

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
| `-OutputFile <путь>` | да | Путь к выходному EPF/ERF-файлу |

> `*` — нужен либо `-InfoBasePath`, либо пара `-InfoBaseServer` + `-InfoBaseRef`

## Коды возврата

| Код | Описание                    |
|-----|-----------------------------|
| 0   | Успешная сборка             |
| 1   | Ошибка (см. лог)           |

## Ссылочные типы

Если обработка использует ссылочные типы конфигурации (`CatalogRef.XXX`, `DocumentRef.XXX`) — сборка в пустой базе упадёт с ошибкой XDTO. Зарегистрируй базу с целевой конфигурацией через `/db-list add`.

## Примеры

```powershell
# Сборка обработки (файловая база)
powershell.exe -NoProfile -File .claude/skills/epf-build/scripts/epf-build.ps1 -InfoBasePath "C:\Bases\MyDB" -SourceFile "src\МояОбработка.xml" -OutputFile "build\МояОбработка.epf"

# Серверная база
powershell.exe -NoProfile -File .claude/skills/epf-build/scripts/epf-build.ps1 -InfoBaseServer "srv01" -InfoBaseRef "MyDB" -UserName "Admin" -Password "secret" -SourceFile "src\МояОбработка.xml" -OutputFile "build\МояОбработка.epf"
```
