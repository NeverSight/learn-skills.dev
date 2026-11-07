---
name: validate
description: >
  Этот скилл MUST быть вызван для явной валидации любого объекта 1С по запросу пользователя:
  конфигурация (CF), расширение (CFE), объект метаданных (meta), управляемая форма (form),
  подсистема (subsystem), командный интерфейс (interface), роль (role), СКД (skd),
  MXL-макет (mxl), внешняя обработка (epf), внешний отчёт (erf).
  SHOULD также вызывать после compile/edit/init/borrow операций при необходимости ручной проверки.
  Do NOT вызывать вручную после автоматических операций — валидация выполняется в соответствующих скиллах.
argument-hint: <ObjectType> <ObjectPath> [options]
allowed-tools:
  - Bash
  - Read
  - Glob
---

# /validate — валидация объектов 1С

Универсальный валидатор XML-структур. Выбери раздел по типу объекта.

---

## CF — конфигурация

Проверяет `Configuration.xml`: XML well-formedness, InternalInfo, свойства, enum-значения, ChildObjects, DefaultLanguage, файлы языков, каталоги объектов.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/cf-validate.ps1 -ConfigPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `ConfigPath` | Путь к Configuration.xml или каталогу выгрузки |
| `MaxErrors` | Лимит ошибок (default: 30) |
| `OutFile` | Записать результат в файл (UTF-8 BOM) |

Проверки (8): root structure, InternalInfo, Properties, enum-значения (11 свойств), ChildObjects (44 типа), DefaultLanguage, файлы языков, каталоги объектов.

---

## CFE — расширение конфигурации

Проверяет расширение: XML-формат, свойства Extension, состав, заимствованные объекты.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/cfe-validate.ps1 -ExtensionPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `ExtensionPath` | Путь к каталогу или Configuration.xml расширения |
| `MaxErrors` | Лимит ошибок (default: 30) |
| `OutFile` | Записать результат в файл |

Проверки (9): root structure, InternalInfo, Extension properties (ObjectBelonging, NamePrefix, KeepMapping), enum-значения, ChildObjects, DefaultLanguage, файлы языков, каталоги объектов, заимствованные объекты.

---

## Meta — объект метаданных

Поддерживаемые типы (23): Catalog, Document, Enum, ExchangePlan, ChartOfAccounts, ChartOfCharacteristicTypes, ChartOfCalculationTypes, BusinessProcess, Task, InformationRegister, AccumulationRegister, AccountingRegister, CalculationRegister, Report, DataProcessor, CommonModule, ScheduledJob, EventSubscription, HTTPService, WebService, Constant, DocumentJournal, DefinedType.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/meta-validate.ps1 -ObjectPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `ObjectPath` | Путь к XML-файлу или каталогу объекта (авторезолв) |
| `MaxErrors` | Лимит ошибок (default: 30) |
| `OutFile` | Записать результат в файл |

Проверки (11): root structure, InternalInfo/GeneratedType, Properties (Name/Synonym), enum-значения, StandardAttributes, ChildObjects, Attributes/Dimensions/Resources (UUID, Name, Type), уникальность имён, TabularSections, кросс-свойства, HTTPService/WebService вложенная структура.

---

## Form — управляемая форма

Проверяет `Form.xml`: уникальность ID, companion-элементы, ссылки DataPath, команды.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/form-validate.ps1 -FormPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `FormPath` | Путь к Form.xml |
| `MaxErrors` | Лимит ошибок (default: 30) |

Проверки (11): корневой элемент Form, AutoCommandBar, уникальность ID элементов, уникальность ID реквизитов, уникальность ID команд, companion-элементы, DataPath→реквизит, CommandName→команда, события, Command actions, MainAttribute.

---

## Subsystem — подсистема

Проверяет XML подсистемы из выгрузки конфигурации.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/subsystem-validate.ps1 -SubsystemPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `SubsystemPath` | Путь к XML-файлу подсистемы |
| `MaxErrors` | Лимит ошибок (default: 30) |
| `OutFile` | Записать результат в файл |

Проверки (13): root structure, 9 обязательных свойств, Name идентификатор, Synonym, булевы свойства, Content (xr:Item, xsi:type), дубликаты Content, ChildObjects, дубликаты ChildObjects, файлы ChildObjects, CommandInterface.xml, Picture, UseOneCommand→1 элемент.

---

## Interface — командный интерфейс

Проверяет `CommandInterface.xml`: корневой элемент, секции, порядок, ссылки на команды, дубликаты.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/interface-validate.ps1 -CIPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `CIPath` | Путь к CommandInterface.xml |
| `MaxErrors` | Лимит ошибок (default: 30) |
| `OutFile` | Записать результат в файл |

Проверки (13): root structure, допустимые дочерние элементы (5 секций), порядок секций, дубликаты секций, CommandsVisibility, дубликаты CommandsVisibility, CommandsPlacement, CommandsOrder, SubsystemsOrder, дубликаты SubsystemsOrder, GroupsOrder, дубликаты GroupsOrder, формат ссылок на команды.

---

## Role — роль 1С

Проверяет `Rights.xml`: namespace, глобальные флаги, типы объектов, имена прав, RLS, шаблоны. Опционально — метаданные роли.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/role-validate.ps1 -RightsPath "<путь>" [-MetadataPath "<путь>"]
```

| Параметр | Описание |
|----------|----------|
| `RightsPath` | Путь к Rights.xml |
| `MetadataPath` | Путь к Roles/ИмяРоли.xml (опционально) |
| `OutFile` | Записать результат в файл |

Проверки: XML well-formed, `<Rights>` + namespace, 3 глобальных флага, `<object>` (name, тип, права), вложенные объекты, RLS `<restrictionByCondition>`, шаблоны `<restrictionTemplate>`. Метаданные (если указаны): `<Role>`, UUID, Name, Synonym.

**Важно:** для кириллических путей использовать `-OutFile` и читать результат через Read tool.

---

## SKD — схема компоновки данных

Проверяет `Template.xml` схемы компоновки данных: формат, битые ссылки, дубликаты.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/skd-validate.ps1 -TemplatePath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `TemplatePath` | Путь к Template.xml или каталогу (авторезолв в `Ext/Template.xml`) |
| `MaxErrors` | Лимит ошибок (default: 20) |
| `OutFile` | Записать результат в файл |

Проверки (~30): Root (XML, DataCompositionSchema, namespace), DataSource (name, type, уникальность), DataSet (xsi:type, name, dataSource, query), Fields (dataPath, field, уникальность), Links (source/dest, expressions), CalcFields/TotalFields, Parameters, Templates, GroupTemplates, Variants, Settings.

---

## MXL — макет табличного документа

Проверяет `Template.xml` на структурные ошибки: индексы строк/форматов/шрифтов/границ, ссылки на наборы колонок, именованные области.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/mxl-validate.ps1 -TemplatePath "<путь>"
```

Или по имени обработки/макета:
```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/mxl-validate.ps1 -ProcessorName "<Имя>" -TemplateName "<Макет>" [-SrcDir "<каталог>"]
```

| Параметр | Описание |
|----------|----------|
| `TemplatePath` | Прямой путь к Template.xml |
| `ProcessorName` | Имя обработки (альтернатива пути) |
| `TemplateName` | Имя макета (альтернатива пути) |
| `SrcDir` | Каталог исходников (default: `src`) |
| `MaxErrors` | Лимит ошибок (default: 20) |

Проверки (12): height, vgRows, индексы форматов ячеек, formatIndex строк/колонок, индексы колонок в ячейках, columnsID строк, columnsID merge/namedItem, диапазоны namedItem, диапазоны объединений, индексы шрифтов, индексы линий границ, pictureIndex.

---

## EPF — внешняя обработка

Проверяет XML-исходники: root structure, InternalInfo, Properties, ChildObjects, реквизиты, табличные части, уникальность имён, файлы форм и макетов.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/epf-validate.ps1 -ObjectPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `ObjectPath` | Путь к корневому XML или каталогу обработки (авторезолв) |
| `MaxErrors` | Лимит ошибок (default: 30) |
| `OutFile` | Записать результат в файл |

Проверки (10): root structure (ExternalDataProcessor), InternalInfo, Properties (Name, Synonym), ChildObjects, Cross-references (DefaultForm), Attributes (UUID, Name, Type), TabularSections, уникальность имён, файлы форм/макетов, дескрипторы форм.

---

## ERF — внешний отчёт

Использует тот же скрипт, что и EPF — автоопределение по типу элемента (ExternalReport). Дополнительно проверяет `MainDataCompositionSchema`.

```powershell
powershell.exe -NoProfile -File .claude/skills/validate/scripts/epf-validate.ps1 -ObjectPath "<путь>"
```

| Параметр | Описание |
|----------|----------|
| `ObjectPath` | Путь к корневому XML или каталогу отчёта (авторезолв) |
| `MaxErrors` | Лимит ошибок (default: 30) |
| `OutFile` | Записать результат в файл |

Проверки (10): root structure (ExternalReport), InternalInfo, Properties (Name, Synonym, MainDataCompositionSchema), ChildObjects, Cross-references (DefaultForm, MainDCS→Template), Attributes, TabularSections, уникальность имён, файлы, дескрипторы форм.

---

## Коды возврата

| Код | Значение |
|-----|----------|
| 0 | Все проверки пройдены (возможны предупреждения) |
| 1 | Есть ошибки |
