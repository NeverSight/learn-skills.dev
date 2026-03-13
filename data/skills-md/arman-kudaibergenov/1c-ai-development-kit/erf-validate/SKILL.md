---
name: erf-validate
description: Валидация внешнего отчёта 1С (ERF). Используй после создания или модификации отчёта для проверки корректности
argument-hint: <ObjectPath> [-MaxErrors 30]
allowed-tools:
  - Bash
  - Read
  - Glob
---

# /erf-validate — валидация внешнего отчёта (ERF)

Проверяет структурную корректность XML-исходников внешнего отчёта: корневую структуру, InternalInfo, свойства (включая MainDataCompositionSchema), ChildObjects, реквизиты, табличные части, уникальность имён, наличие файлов форм и макетов.

Использует тот же скрипт, что и `/epf-validate` — автоопределение по типу элемента (ExternalReport).

## Использование

```
/erf-validate <ObjectPath>
```

## Параметры

| Параметр   | Обязательный | По умолчанию | Описание                                      |
|------------|:------------:|--------------|-------------------------------------------------|
| ObjectPath | да           | —            | Путь к корневому XML или каталогу отчёта        |
| MaxErrors  | нет          | 30           | Остановиться после N ошибок                     |
| OutFile    | нет          | —            | Записать результат в файл (UTF-8 BOM)           |

`ObjectPath` авторезолв: если указана директория — ищет `<dirName>/<dirName>.xml`.

## Команда

```powershell
powershell.exe -NoProfile -File .claude/skills/epf-validate/scripts/epf-validate.ps1 -ObjectPath "<путь>"
```

## Выполняемые проверки

| #  | Проверка                                              | Серьёзность  |
|----|-------------------------------------------------------|--------------|
| 1  | Root structure: MetaDataObject/ExternalReport          | ERROR        |
| 2  | InternalInfo: ClassId, ContainedObject, GeneratedType  | ERROR / WARN |
| 3  | Properties: Name, Synonym, MainDataCompositionSchema   | ERROR / WARN |
| 4  | ChildObjects: допустимые типы, порядок                 | ERROR / WARN |
| 5  | Cross-references: DefaultForm, MainDCS → Template      | ERROR / WARN |
| 6  | Attributes: UUID, Name, Type                           | ERROR        |
| 7  | TabularSections: UUID, Name, GeneratedType, Attributes | ERROR / WARN |
| 8  | Уникальность имён (Attribute, TS, Form, Template, Command) | ERROR   |
| 9  | Файлы: формы (.xml + Ext/Form.xml), макеты            | ERROR        |
| 10 | Дескрипторы форм: корневая структура, uuid, Name, FormType | ERROR / WARN |

## Вывод

```
=== Validation: ERF.МойОтчёт ===

[OK]    1. Root structure: MetaDataObject/ExternalReport, version 2.17
[OK]    2. InternalInfo: ClassId correct, 1 GeneratedType
[OK]    3. Properties: Name="МойОтчёт", Synonym present, MainDCS set
[OK]    4. ChildObjects: Form(1), Template(1)
[OK]    5. Cross-references: DefaultForm, MainDCS valid
[OK]    6. Attributes: none
[OK]    7. TabularSections: none
[OK]    8. Name uniqueness: 2 names, all unique
[OK]    9. File existence: 4 files verified
[OK]    10. Form descriptors: 1 checked

=== Result: 0 errors, 0 warnings ===
```

Код возврата: 0 = все проверки пройдены, 1 = есть ошибки.

## Верификация

```
/erf-init <Name> --with-skd        — создать отчёт с СКД
/erf-validate src/<Name>.xml        — проверить результат
/erf-build <Name>                   — собрать ERF
```

## Когда использовать

- **После `/erf-init`**: проверить scaffold
- **После добавления формы/макета/СКД**: убедиться что ChildObjects и MainDCS корректны
- **После ручного редактирования XML**: выявить структурные ошибки до сборки
- **При отладке сборки**: найти причину ошибки Designer
