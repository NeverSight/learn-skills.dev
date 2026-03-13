---
name: epf-validate
description: Валидация внешней обработки 1С (EPF). Используй после создания или модификации обработки для проверки корректности
argument-hint: <ObjectPath> [-MaxErrors 30]
allowed-tools:
  - Bash
  - Read
  - Glob
---

# /epf-validate — валидация внешней обработки (EPF)

Проверяет структурную корректность XML-исходников внешней обработки: корневую структуру, InternalInfo, свойства, ChildObjects, реквизиты, табличные части, уникальность имён, наличие файлов форм и макетов.

Скрипт также работает для внешних отчётов (ERF) — автоопределение по типу элемента. См. `/erf-validate`.

## Использование

```
/epf-validate <ObjectPath>
```

## Параметры

| Параметр   | Обязательный | По умолчанию | Описание                                      |
|------------|:------------:|--------------|-------------------------------------------------|
| ObjectPath | да           | —            | Путь к корневому XML или каталогу обработки     |
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
| 1  | Root structure: MetaDataObject/ExternalDataProcessor   | ERROR        |
| 2  | InternalInfo: ClassId, ContainedObject, GeneratedType  | ERROR / WARN |
| 3  | Properties: Name (identifier), Synonym                 | ERROR / WARN |
| 4  | ChildObjects: допустимые типы, порядок                 | ERROR / WARN |
| 5  | Cross-references: DefaultForm → Form, AuxiliaryForm    | ERROR / WARN |
| 6  | Attributes: UUID, Name, Type                           | ERROR        |
| 7  | TabularSections: UUID, Name, GeneratedType, Attributes | ERROR / WARN |
| 8  | Уникальность имён (Attribute, TS, Form, Template, Command) | ERROR   |
| 9  | Файлы: формы (.xml + Ext/Form.xml), макеты            | ERROR        |
| 10 | Дескрипторы форм: корневая структура, uuid, Name, FormType | ERROR / WARN |

## Вывод

```
=== Validation: EPF.МояОбработка ===

[OK]    1. Root structure: MetaDataObject/ExternalDataProcessor, version 2.17
[OK]    2. InternalInfo: ClassId correct, 1 GeneratedType
[OK]    3. Properties: Name="МояОбработка", Synonym present, DefaultForm set
[OK]    4. ChildObjects: Attribute(3), TabularSection(1), Form(1)
[OK]    5. Cross-references: DefaultForm valid
[OK]    6. Attributes: 3 checked (UUID, Name, Type)
[OK]    7. TabularSections: 1 sections, 5 inner attributes
[OK]    8. Name uniqueness: 6 names, all unique
[OK]    9. File existence: 3 files verified
[OK]    10. Form descriptors: 1 checked

=== Result: 0 errors, 0 warnings ===
```

Код возврата: 0 = все проверки пройдены, 1 = есть ошибки.

## Верификация

```
/epf-init <Name>                   — создать обработку
/epf-validate src/<Name>.xml       — проверить результат
/epf-build <Name>                  — собрать EPF
```

## Когда использовать

- **После `/epf-init`**: проверить scaffold
- **После добавления формы/макета**: убедиться что ChildObjects, файлы и ссылки корректны
- **После ручного редактирования XML**: выявить структурные ошибки до сборки
- **При отладке сборки**: найти причину ошибки Designer
