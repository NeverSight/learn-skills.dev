---
name: erf-expert
description: >
  Этот скилл MUST быть вызван для всех операций с внешними отчётами 1С (ERF):
  создание (init), сборка (build), разборка (dump).
  SHOULD также вызывать при любой работе с ERF-файлами и их исходниками.
  Do NOT использовать для внешних обработок (EPF) — используй epf-expert;
  для СКД внутри отчёта — используй skd-edit; для форм — form-add.
argument-hint: "<mode> [args...]  # modes: init|build|dump"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /erf-expert — Внешние отчёты 1С (ERF)

Единый скилл для всех операций с внешними отчётами ERF. Выбери нужный режим:

| Режим | Что делает |
|-------|-----------|
| `init` | Создать новый пустой отчёт (scaffold XML) |
| `build` | Собрать ERF из XML-исходников |
| `dump` | Разобрать ERF в XML-исходники |

---

## Режим: init — создание отчёта

Генерирует минимальный набор XML-исходников для внешнего отчёта (ERF) 1С.

### Usage

```
/erf-expert init <Name> [Synonym] [SrcDir] [--with-skd]
```

| Параметр  | Обязательный | По умолчанию | Описание |
|-----------|:------------:|--------------|----------|
| Name      | да           | —            | Имя отчёта |
| Synonym   | нет          | = Name       | Синоним (отображаемое имя) |
| SrcDir    | нет          | `src`        | Каталог исходников |
| --WithSKD | нет          | —            | Создать пустую СКД и привязать к MainDataCompositionSchema |

### Команда

```powershell
powershell.exe -NoProfile -File .claude/skills/erf-expert/scripts/erf-init.ps1 -Name "<Name>" [-Synonym "<Synonym>"] [-SrcDir "<SrcDir>"] [-WithSKD]
```

### Что создаётся

```
<SrcDir>/
├── <Name>.xml          # Корневой файл метаданных (4 UUID)
└── <Name>/
    └── Ext/
        └── ObjectModule.bsl  # Модуль объекта с 3 регионами
```

При `--WithSKD` дополнительно:

```
<SrcDir>/<Name>/
    Templates/
    ├── ОсновнаяСхемаКомпоновкиДанных.xml
    └── ОсновнаяСхемаКомпоновкиДанных/Ext/Template.xml  # Пустая СКД
```

- Корневой XML содержит `MetaDataObject/ExternalReport`
- При `--WithSKD`: `MainDataCompositionSchema` заполняется, `ChildObjects` содержит `<Template>`
- ClassId фиксирован: `e41aff26-25cf-4bb6-b6c1-3f478a75f374`
- Файлы создаются в UTF-8 с BOM

### Дальнейшие шаги

- Добавить форму: `/form-add`
- Добавить макет: `/mxl-expert template-add`
- Редактировать СКД: `/skd-edit`
- Добавить справку: `/help-add`
- Собрать ERF: `/erf-expert build`

---

## Режим: build — сборка ERF

Собирает ERF файл из XML-исходников с помощью платформы 1С.

### Usage

```
/erf-expert build <Name> [SrcDir] [OutDir]
```

| Параметр | Обязательный | По умолчанию | Описание |
|----------|:------------:|--------------|----------|
| Name     | да           | —            | Имя объекта (имя корневого XML) |
| SrcDir   | нет          | `src`        | Каталог исходников |
| OutDir   | нет          | `build`      | Каталог для результата |

### Параметры подключения

Прочитай `.v8-project.json` из корня проекта. Возьми `v8path` и разреши базу:
1. Если пользователь указал параметры (путь, сервер) — используй напрямую
2. Если указал базу по имени — ищи в `.v8-project.json`
3. Если не указал — сопоставь ветку Git с `databases[].branches`
4. Если ветка не совпала — используй `default`
5. Если `.v8-project.json` нет — создай пустую ИБ в `./base`

Если `v8path` не задан: `Get-ChildItem "C:\Program Files\1cv8\*\bin\1cv8.exe" | Sort -Desc | Select -First 1`

### Команда

```powershell
powershell.exe -NoProfile -File .claude/skills/erf-expert/scripts/erf-build.ps1 -InfoBasePath "<путь>" -SourceFile "src\<Name>.xml" -OutputFile "build\<Name>.erf"
```

| Параметр | Обязательный | Описание |
|----------|:------------:|----------|
| `-V8Path <путь>` | нет | Каталог bin платформы |
| `-InfoBasePath <путь>` | * | Файловая база |
| `-InfoBaseServer <сервер>` | * | Сервер 1С |
| `-InfoBaseRef <имя>` | * | Имя базы на сервере |
| `-UserName <имя>` | нет | Пользователь |
| `-Password <пароль>` | нет | Пароль |
| `-SourceFile <путь>` | да | Корневой XML исходников |
| `-OutputFile <путь>` | да | Выходной ERF файл |

> `*` — нужен либо `-InfoBasePath`, либо пара `-InfoBaseServer` + `-InfoBaseRef`

---

## Режим: dump — разборка ERF

Разбирает ERF файл в XML-исходники с помощью платформы 1С (иерархический формат).

### Usage

```
/erf-expert dump <File> [OutDir]
```

| Параметр | Обязательный | По умолчанию | Описание |
|----------|:------------:|--------------|----------|
| File     | да           | —            | Путь к ERF файлу |
| OutDir   | нет          | `src`        | Каталог для выгрузки исходников |

### Параметры подключения

Аналогично режиму `build` — разрешение базы через `.v8-project.json`.

### Команда

```powershell
powershell.exe -NoProfile -File .claude/skills/erf-expert/scripts/erf-dump.ps1 -InfoBasePath "<путь>" -InputFile "<файл>.erf" -OutputDir "src"
```

| Параметр | Обязательный | Описание |
|----------|:------------:|----------|
| `-V8Path <путь>` | нет | Каталог bin платформы |
| `-InfoBasePath <путь>` | * | Файловая база |
| `-InfoBaseServer <сервер>` | * | Сервер 1С |
| `-InfoBaseRef <имя>` | * | Имя базы на сервере |
| `-UserName <имя>` | нет | Пользователь |
| `-Password <пароль>` | нет | Пароль |
| `-InputFile <путь>` | да | Путь к ERF файлу |
| `-OutputDir <путь>` | да | Каталог для выгрузки |
| `-Format <формат>` | нет | `Hierarchical` (по умолч.) / `Plain` |

### Структура результата (Hierarchical)

```
<OutDir>/
├── <Name>.xml
└── <Name>/
    ├── Ext/
    │   └── ObjectModule.bsl
    ├── Forms/
    │   ├── <FormName>.xml
    │   └── <FormName>/Ext/Form.xml
    └── Templates/
        ├── <TemplateName>.xml
        └── <TemplateName>/Ext/Template.<ext>
```
