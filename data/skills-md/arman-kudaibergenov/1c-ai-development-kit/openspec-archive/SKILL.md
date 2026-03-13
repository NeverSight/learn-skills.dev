---
name: openspec-archive
description: "Архивировать завершённое OpenSpec изменение и обновить спецификации."
argument-hint: <change-id>
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /openspec-archive — Архивация изменения

**Steps**
1. Определи change-id для архивации:
   - Из аргументов $ARGUMENTS
   - Или посмотри `openspec/changes/` и уточни у пользователя
2. Проверь что change завершён (все задачи в tasks.md отмечены [x])
3. Перемести `openspec/changes/<id>/` в `openspec/changes/archive/<id>/`
4. Если есть spec deltas — обнови соответствующие спецификации в `openspec/specs/`
5. Валидируй результат

**Reference**
- Проверь список изменений: `ls openspec/changes/`
- Проверь спеки: `ls openspec/specs/`
